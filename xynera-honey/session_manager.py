import uuid
import json
import os
from datetime import datetime

from fake_filesystem import create_filesystem
from service_manager import ServiceManager

HOME_DIR = "/home/ubuntu"
DEFAULT_HOSTNAME = "web-prod-01"
DEFAULT_USERNAME = "ubuntu"
DEFAULT_GROUPS = ["ubuntu", "sudo", "docker"]
DEFAULT_KERNEL = "5.15.0-82-generic"

DEFAULT_PERSONALITY = {
    "name": "Standard Ubuntu Server",
    "hostname": DEFAULT_HOSTNAME,
    "user": DEFAULT_USERNAME,
    "groups": DEFAULT_GROUPS,
    "home_dir": HOME_DIR,
    "shell": "/bin/bash",
}


class SessionManager:
    def __init__(self, attacker_ip):
        self.session_id = str(uuid.uuid4())
        self.attacker_ip = attacker_ip
        self.cwd = HOME_DIR
        self.command_history = []
        self.attack_types = []
        self.threat_score = 0
        self.is_active = True
        self.start_time = datetime.now().isoformat()
        self.end_time = None

        # Per-session dynamic filesystem (touch/mkdir/rm/mv/cp persist for
        # the life of this session only, never leaking into other sessions).
        self.filesystem = create_filesystem()

        # Per-session fake service state (nginx/mysql/redis/ssh/docker),
        # so `service <n> stop`, `systemctl status <n>`, `netstat`, and
        # `ss` all agree with each other for this attacker.
        self.service_manager = ServiceManager()
        self.services = self.service_manager

        self.personality = {}
        self.hostname = DEFAULT_HOSTNAME
        self.username = DEFAULT_USERNAME
        self.groups = list(DEFAULT_GROUPS)
        self.home_dir = HOME_DIR
        self.shell = "/bin/bash"
        self.kernel_version = DEFAULT_KERNEL
        self.environment = {}
        self.backend_cache = {
            "filesystem": {},
            "responses": {},
            "identity": {},
            "services": {},
            "metadata": {
                "session_id": self.session_id,
                "attacker_ip": self.attacker_ip,
            },
        }

        self.session = {
            "session_id": self.session_id,
            "attacker_ip": self.attacker_ip,
            "start_time": self.start_time,
            "end_time": None,
            "cwd": self.cwd,
            "filesystem": self.filesystem,
            "backend_cache": self.backend_cache,
            "hostname": self.hostname,
            "username": self.username,
            "groups": self.groups,
            "personality": self.personality,
            "environment": self.environment,
            "service_manager": self.service_manager,
            "command_history": self.command_history,
            "attack_types": self.attack_types,
            "threat_score": self.threat_score,
            "is_active": True,
            # Tracks the deception engine's rolling read on attacker intent
            # (recon / credential / malware) so responses can adapt across
            # a session rather than per-command in isolation.
            "attacker_profile": {"intent": "recon"},
        }
        self.apply_personality(DEFAULT_PERSONALITY)
        self.sync_service_state()

    def get_session(self):
        return self.session

    def get_cwd(self):
        return self.cwd

    def get_filesystem(self):
        return self.filesystem

    def get_services(self):
        return self.service_manager

    def change_directory(self, path):
        self.cwd = path
        self.environment["PWD"] = path
        self.session["cwd"] = path
        self.session["environment"] = self.environment
        self.backend_cache["metadata"]["cwd"] = path

    def add_command(self, command):
        self.command_history.append({
            "command": command,
            "timestamp": datetime.now().isoformat(),
            "cwd": self.cwd
        })

    def add_attack_type(self, attack_type):
        if attack_type not in self.attack_types:
            self.attack_types.append(attack_type)

    def update_threat_score(self, score):
        self.threat_score += score
        self.session["threat_score"] = self.threat_score

    def sync_service_state(self):
        self.backend_cache["services"] = {
            name: dict(info)
            for name, info in self.service_manager.services.items()
        }

    def sync_backend_after_filesystem_write(self):
        # Filesystem mutations can affect many read keys (ls/cat/cd/pwd), so
        # the safest synchronization boundary is to clear stale backend reads.
        self.invalidate_backend()

    def backend_exists(self, path):
        return path in self.backend_cache["filesystem"]

    def get_backend(self, path, default=None):
        return self.backend_cache["filesystem"].get(path, default)

    def save_backend(self, path, data):
        self.backend_cache["filesystem"][path] = data
        return data

    def preload_backend(self, path, content):
        """Pre-seed the backend cache with dataset content for a given path.

        Calling this before the attacker reads `path` ensures the cache
        returns the injected content rather than the FakeFilesystem default.
        Invalidates any previously cached value for that path first so
        preloads are always fresh.
        """
        self.invalidate_backend(path)
        return self.save_backend(path, content)

    def invalidate_backend(self, path=None):
        if path is None:
            self.backend_cache["filesystem"].clear()
            return
        self.backend_cache["filesystem"].pop(path, None)

    def response_exists(self, command):
        return command in self.backend_cache["responses"]

    def get_response(self, command, default=None):
        return self.backend_cache["responses"].get(command, default)

    def save_response(self, command, response):
        self.backend_cache["responses"][command] = response
        return response

    def _sync_identity_cache(self):
        self.backend_cache["identity"] = {
            "hostname": self.hostname,
            "username": self.username,
            "groups": list(self.groups),
            "kernel_version": self.kernel_version,
            "personality": dict(self.personality),
            "environment": dict(self.environment),
        }
        self.backend_cache["responses"].clear()
        self.invalidate_backend()

    def apply_personality(self, personality=None):
        personality = self._normalize_personality(personality)
        old_home = self.home_dir
        old_username = self.username

        self.personality = personality
        self.hostname = personality["hostname"]
        self.username = personality["user"]
        self.groups = list(personality["groups"])
        self.home_dir = personality["home_dir"]
        self.shell = personality["shell"]
        self.kernel_version = personality.get("kernel", DEFAULT_KERNEL)
        self.environment = self._build_environment()

        if old_home != self.home_dir:
            self._move_home_directory(old_home, self.home_dir)
            if self.cwd == old_home or self.cwd.startswith(old_home + "/"):
                self.change_directory(self.home_dir + self.cwd[len(old_home):])
        else:
            self.change_directory(self.cwd)

        self._sync_identity_files(old_username)
        self._apply_ownership(self.home_dir, self.username, self.groups[0])
        self._sync_session_identity()
        self._sync_identity_cache()

    def _normalize_personality(self, personality):
        data = dict(DEFAULT_PERSONALITY)
        if isinstance(personality, dict):
            data.update(personality)
        elif isinstance(personality, str):
            data["name"] = personality

        username = data.get("user") or data.get("username") or self.username
        hostname = data.get("hostname") or self.hostname
        groups = data.get("groups") or [username]
        if isinstance(groups, str):
            groups = groups.split()

        data["user"] = username
        data["hostname"] = hostname
        data["groups"] = list(groups)
        data["home_dir"] = data.get("home_dir") or (
            "/root" if username == "root" else f"/home/{username}"
        )
        data["shell"] = data.get("shell") or "/bin/bash"
        return data

    def _build_environment(self):
        return {
            "SHELL": self.shell,
            "PWD": self.cwd,
            "LOGNAME": self.username,
            "HOME": self.home_dir,
            "LANG": "en_US.UTF-8",
            "TERM": "xterm-256color",
            "USER": self.username,
            "SHLVL": "1",
            "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
            "_": "/usr/bin/env",
        }

    def _move_home_directory(self, old_home, new_home):
        old_node = self.filesystem.get_node(old_home)
        new_node = self.filesystem.get_node(new_home)

        if old_node is not None and new_node is not None:
            if hasattr(old_node, "children") and hasattr(new_node, "children"):
                for child in list(old_node.children.values()):
                    if child.name in new_node.children:
                        new_node.remove_child(child.name)
                    old_node.remove_child(child.name)
                    new_node.add_child(child)
                if old_node.parent is not None:
                    old_node.parent.remove_child(old_node.name)
            return

        if old_node is not None:
            self.filesystem.mv("/", old_home, new_home)
            return
        parent = os.path.dirname(new_home.rstrip("/")) or "/"
        if self.filesystem.exists(parent):
            self.filesystem.mkdir("/", new_home)

    def _sync_identity_files(self, old_username):
        self._write_file("/etc/hostname", f"{self.hostname}\n")
        self._write_file("/etc/hosts", self._render_hosts())
        self._write_file("/etc/passwd", self._render_passwd(old_username))

    def _render_hosts(self):
        existing = self.filesystem.cat("/", "/etc/hosts")
        if existing.startswith("cat:"):
            existing = "127.0.0.1 localhost\n"
        lines = [
            line for line in existing.splitlines()
            if not line.startswith("127.0.1.1 ")
        ]
        lines.append(f"127.0.1.1 {self.hostname}")
        return "\n".join(lines) + "\n"

    def _render_passwd(self, old_username):
        existing = self.filesystem.cat("/", "/etc/passwd")
        if existing.startswith("cat:"):
            existing = "root:x:0:0:root:/root:/bin/bash\n"

        if self.username == "root":
            uid = gid = 0
            full_name = "root"
        else:
            uid = gid = 1000
            full_name = self.personality.get("name", self.username.title())

        replacement = (
            f"{self.username}:x:{uid}:{gid}:{full_name}:"
            f"{self.home_dir}:{self.shell}"
        )
        lines = []
        replaced = False
        for line in existing.splitlines():
            if not line:
                continue
            account = line.split(":", 1)[0]
            if account in {old_username, self.username} and account != "root":
                if not replaced:
                    lines.append(replacement)
                    replaced = True
                continue
            if account == "root" and self.username == "root":
                lines.append(replacement)
                replaced = True
                continue
            lines.append(line)

        if not replaced:
            lines.append(replacement)
        return "\n".join(lines) + "\n"

    def _write_file(self, path, content):
        if not self.filesystem.exists(path):
            self.filesystem.touch("/", path)
        node = self.filesystem.get_node(path)
        if node is not None and hasattr(node, "content"):
            node.content = content
            node.metadata.touch()

    def _apply_ownership(self, path, owner, group):
        node = self.filesystem.get_node(path)
        if node is None:
            return
        node.owner = owner
        node.group = group
        if hasattr(node, "children"):
            for child in node.children.values():
                self._apply_ownership(child.path(), owner, group)

    def _sync_session_identity(self):
        self.session.update({
            "cwd": self.cwd,
            "hostname": self.hostname,
            "username": self.username,
            "groups": self.groups,
            "personality": self.personality,
            "environment": self.environment,
            "service_manager": self.service_manager,
        })

    def close_session(self):
        # Bug fix: close_session() could previously be invoked more than
        # once (e.g. an exception during cleanup triggering a second call),
        # which re-exported the session and overwrote its end_time / duration.
        # Once closed, further calls are a no-op.
        if not self.is_active:
            return
        self.is_active = False
        self.end_time = datetime.now().isoformat()
        self.session["is_active"] = False
        self.session["end_time"] = self.end_time
        self.export_session()

    def export_session(self):
        """Persist the completed session to disk as JSON for replay/analysis."""
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        start = datetime.fromisoformat(self.start_time)
        end = datetime.fromisoformat(self.end_time)
        duration = str(end - start)

        session_data = {
            "session_id": self.session_id,
            "ip": self.attacker_ip,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "current_directory": self.cwd,
            "hostname": self.hostname,
            "username": self.username,
            "groups": self.groups,
            "personality": self.personality,
            "environment": self.environment,
            "commands": self.command_history,
            "threat_score": self.threat_score,
            "attack_types": self.attack_types,
            "attacker_profile": self.session["attacker_profile"],
            "session_duration": duration
        }

        filename = f"{log_dir}/session_{self.session_id}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(session_data, f, indent=4)

        print(f"[+] Session exported -> {filename}")

    def summary(self):
        return {
            "session_id": self.session_id,
            "attacker_ip": self.attacker_ip,
            "current_directory": self.cwd,
            "hostname": self.hostname,
            "username": self.username,
            "commands_executed": len(
                self.command_history
            ),
            "attack_types": self.attack_types,
            "threat_score": self.threat_score,
            "is_active": self.is_active
        }
