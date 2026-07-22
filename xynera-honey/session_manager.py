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
        # Per-session dynamic filesystem (touch/mkdir/rm/mv/cp persist for
        # the life of this session only, never leaking into other sessions).
        self.filesystem = create_filesystem()

        # Per-session fake service state (nginx/mysql/redis/ssh/docker),
        # so `service <n> stop`, `systemctl status <n>`, `netstat`, and
        # `ss` all agree with each other for this attacker.
        self.services = ServiceManager()

        # Backend-facing caches: per-session storage for anything the AI
        # backend supplies (dynamic file content, precomputed command
        # responses, identity snapshots, service snapshots). Kept separate
        # from `self.session` because it's write-through/cache semantics
        # rather than session metadata.
        self.backend_cache = {
            "filesystem": {},
            "responses": {},
            "identity": {},
            "services": {},
            "metadata": {
                "attacker_ip": attacker_ip,
            },
        }

        # Dynamic per-attacker hostname: derived from the attacker's own
        # IP so different attackers land on visibly different-looking
        # hosts instead of everyone seeing the same static "web-prod-01"
        # (falls back to the static default if no IP is available).
        dynamic_hostname = (
            f"node-{attacker_ip.split('.')[-1]}" if attacker_ip else DEFAULT_HOSTNAME
        )

        self.session = {
            "session_id": str(uuid.uuid4()),
            "attacker_ip": attacker_ip,
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "cwd": HOME_DIR,
            "command_history": [],
            "attack_types": [],
            "threat_score": 0,
            "is_active": True,
            # Tracks the deception engine's rolling read on attacker intent
            # (recon / credential / malware) so responses can adapt across
            # a session rather than per-command in isolation.
            "attacker_profile": {"intent": "recon"},

            # ------------------------------------------------------------
            # Session identity -- the single source of truth for who the
            # attacker currently appears to be logged in as. NOTHING
            # outside this class should hardcode a username, hostname or
            # prompt string; everything reads it via get_prompt() /
            # get_identity(), so that if the identity is ever changed
            # (set_identity()), every future prompt reflects it
            # automatically.
            # ------------------------------------------------------------
            "username": DEFAULT_USERNAME,
            "hostname": dynamic_hostname,
            "groups": list(DEFAULT_GROUPS),
            "home_dir": HOME_DIR,
            "shell": "/bin/bash",
            "kernel_version": DEFAULT_KERNEL,
            "environment": {},
            "service_manager": self.services,

            # Analyst/logging metadata only -- the AI backend's read on
            # what kind of attacker this is. Never surfaced in the
            # attacker-visible prompt or output.
            "personality": None,
        }

        self._sync_environment()
        self._sync_identity_files(old_username=None)
        self._apply_ownership(self.session["home_dir"], self.session["username"], self.session["groups"][0])
        self._sync_identity_cache()
        self.sync_service_state()

    # ------------------------------------------------------------------
    # Attribute-style compatibility shims. `self.session` (the dict) is
    # the single source of truth for identity/environment; these
    # properties just let call sites written as `session_manager.username`
    # / `.hostname` / `.home_dir` / `.groups` / `.kernel_version` /
    # `.environment` / `.service_manager` read (and, where meaningful,
    # write) the same underlying values without a second, divergent copy
    # of the state living on the instance itself.
    # ------------------------------------------------------------------
    @property
    def username(self):
        return self.session["username"]

    @property
    def hostname(self):
        return self.session["hostname"]

    @property
    def home_dir(self):
        return self.session["home_dir"]

    @property
    def groups(self):
        return self.session["groups"]

    @property
    def kernel_version(self):
        return self.session["kernel_version"]

    @property
    def environment(self):
        return self.session["environment"]

    @property
    def service_manager(self):
        return self.services

    # ------------------------------------------------------------------
    # Basic accessors
    # ------------------------------------------------------------------
    def get_session(self):
        return self.session

    def get_cwd(self):
        return self.session["cwd"]

    def get_hostname(self):
        return self.session["hostname"]

    def get_filesystem(self):
        return self.filesystem

    def get_services(self):
        return self.services

    def change_directory(self, path):
        self.session["cwd"] = path
        self.session["environment"]["PWD"] = path
        self.backend_cache["metadata"]["cwd"] = path

    def add_command(self, command):
        self.session["command_history"].append({
            "command": command,
            "timestamp": datetime.now().isoformat(),
            "cwd": self.session["cwd"]
        })

    def add_attack_type(self, attack_type):
        if attack_type not in self.session["attack_types"]:
            self.session["attack_types"].append(attack_type)

    def update_threat_score(self, score):
        self.session["threat_score"] += score

    # ------------------------------------------------------------------
    # PERSONALITY METADATA -- analyst-facing only.
    # Deliberately does NOT touch hostname/username; use set_identity()
    # for that. This only tracks the AI's classification label, purely
    # for logging / session export.
    # ------------------------------------------------------------------
    def update_personality(self, personality_name=None):
        if personality_name:
            self.session["personality"] = personality_name

    # ------------------------------------------------------------------
    # SESSION IDENTITY
    # ------------------------------------------------------------------
    def set_identity(self, username=None, hostname=None, personality=None):
        """
        Changes the attacker-visible identity (username/hostname) and/or
        the analyst-facing personality label.

        Nothing in the current codebase calls this mid-session -- identity
        is assigned once at connection time in __init__() and, in
        practice, stays fixed for the life of the session, which avoids
        ever tipping the attacker off with a shell identity that changes
        mid-conversation. The method exists (rather than being inlined
        into __init__) so that a future AI-backend-driven identity change
        has one single, safe entry point: it keeps every dependent file
        (/etc/hostname, /etc/hosts, /etc/passwd), the environment block,
        and file ownership all in sync instead of only updating the
        prompt string.
        """
        old_username = self.session["username"]

        if username:
            self.session["username"] = username
        if hostname:
            self.session["hostname"] = hostname
        if personality:
            self.session["personality"] = personality

        if username or hostname:
            self._sync_environment()
            self._sync_identity_files(old_username)
            self._apply_ownership(
                self.session["home_dir"], self.session["username"], self.session["groups"][0]
            )
        self._sync_identity_cache()

    def get_identity(self):
        return {
            "username": self.session["username"],
            "hostname": self.session["hostname"],
            "personality": self.session["personality"],
            "cwd": self.session["cwd"],
        }

    def get_prompt(self):
        """
        Builds the shell prompt LIVE from current session state. This is
        the only function that should ever be used to generate the
        prompt string anywhere in the codebase -- never hardcode
        "username@hostname:cwd$" elsewhere. Whatever set_identity() (or
        __init__) last set is what shows up here automatically.
        """
        home = self.session["home_dir"]
        cwd = self.session["cwd"]
        if cwd == home:
            display_path = "~"
        elif cwd.startswith(home + "/"):
            display_path = cwd.replace(home, "~", 1)
        else:
            display_path = cwd
        return f"{self.session['username']}@{self.session['hostname']}:{display_path}$ "

    # ------------------------------------------------------------------
    # Backend cache -- per-session storage for AI-backend-supplied file
    # content and precomputed command responses, so a given path/command
    # resolves consistently for the rest of the session instead of being
    # re-fetched/re-generated on every call.
    # ------------------------------------------------------------------
    def sync_service_state(self):
        self.backend_cache["services"] = {
            name: dict(info)
            for name, info in self.services.services.items()
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
            "hostname": self.session["hostname"],
            "username": self.session["username"],
            "groups": list(self.session["groups"]),
            "kernel_version": self.session["kernel_version"],
            "personality": self.session["personality"],
            "environment": dict(self.session["environment"]),
        }
        self.backend_cache["responses"].clear()
        self.invalidate_backend()

    # ------------------------------------------------------------------
    # Identity <-> filesystem synchronization
    # ------------------------------------------------------------------
    def _sync_environment(self):
        self.session["environment"] = {
            "SHELL": self.session["shell"],
            "PWD": self.session["cwd"],
            "LOGNAME": self.session["username"],
            "HOME": self.session["home_dir"],
            "LANG": "en_US.UTF-8",
            "TERM": "xterm-256color",
            "USER": self.session["username"],
            "SHLVL": "1",
            "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
            "_": "/usr/bin/env",
        }

    def _sync_identity_files(self, old_username):
        """
        Keeps /etc/hostname, /etc/hosts and /etc/passwd inside the real
        simulated filesystem consistent with the session's live identity,
        so `cat`/`ls -l` on those files never shows a stale username or
        hostname after set_identity() changes it.
        """
        self._write_file("/etc/hostname", f"{self.session['hostname']}\n")
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
        lines.append(f"127.0.1.1 {self.session['hostname']}")
        return "\n".join(lines) + "\n"

    def _render_passwd(self, old_username):
        existing = self.filesystem.cat("/", "/etc/passwd")
        if existing.startswith("cat:"):
            existing = "root:x:0:0:root:/root:/bin/bash\n"

        username = self.session["username"]
        home_dir = self.session["home_dir"]
        shell = self.session["shell"]

        if username == "root":
            uid = gid = 0
            full_name = "root"
        else:
            uid = gid = 1000
            full_name = username.title()

        replacement = f"{username}:x:{uid}:{gid}:{full_name}:{home_dir}:{shell}"
        lines = []
        replaced = False
        for line in existing.splitlines():
            if not line:
                continue
            account = line.split(":", 1)[0]
            if old_username and account in {old_username, username} and account != "root":
                if not replaced:
                    lines.append(replacement)
                    replaced = True
                continue
            if account == username and account != "root":
                if not replaced:
                    lines.append(replacement)
                    replaced = True
                continue
            if account == "root" and username == "root":
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

    # ------------------------------------------------------------------
    def close_session(self):
        # Bug fix: close_session() could previously be invoked more than
        # once (e.g. an exception during cleanup triggering a second call),
        # which re-exported the session and overwrote its end_time / duration.
        # Once closed, further calls are a no-op.
        if not self.session["is_active"]:
            return
        self.session["is_active"] = False
        self.session["end_time"] = datetime.now().isoformat()
        self.export_session()

    def export_session(self):
        """Persist the completed session to disk as JSON for replay/analysis."""
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        start = datetime.fromisoformat(self.session["start_time"])
        end = datetime.fromisoformat(self.session["end_time"])
        duration = str(end - start)

        session_data = {
            "session_id": self.session["session_id"],
            "ip": self.session["attacker_ip"],
            "start_time": self.session["start_time"],
            "end_time": self.session["end_time"],
            "current_directory": self.session["cwd"],
            "commands": self.session["command_history"],
            "threat_score": self.session["threat_score"],
            "attack_types": self.session["attack_types"],
            "attacker_profile": self.session["attacker_profile"],
            "session_duration": duration,
            # identity is part of the permanent record too, so if it
            # changed mid-session, that's visible in the logs afterwards.
            "hostname": self.session["hostname"],
            "username": self.session["username"],
            "groups": self.session["groups"],
            # Analyst metadata only -- what the AI classified this
            # attacker/session as, for later review.
            "personality": self.session["personality"],
        }

        filename = f"{log_dir}/session_{self.session['session_id']}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(session_data, f, indent=4)

        print(f"[+] Session exported -> {filename}")

    def summary(self):
        return {
            "session_id": self.session["session_id"],
            "attacker_ip": self.session["attacker_ip"],
            "hostname": self.session["hostname"],
            "username": self.session["username"],
            "current_directory": self.session["cwd"],
            "commands_executed": len(
                self.session["command_history"]
            ),
            "attack_types": self.session["attack_types"],
            "threat_score": self.session["threat_score"],
            "is_active": self.session["is_active"],
            "personality": self.session["personality"],
        }


# ==========================================================
# Multi-Client Session Handling
# ==========================================================
class MultiSessionManager:
    """
    Tracks every live SessionManager, keyed by session_id, so server.py can
    support more than one concurrent attacker connection (each gets its
    own SessionManager -> its own filesystem/services/identity), and so a
    reconnecting IP can be resumed rather than starting a brand new session.
    """

    def __init__(self):
        self.sessions = {}

    def create_session(self, attacker_ip):
        session = SessionManager(attacker_ip)
        self.sessions[session.get_session()["session_id"]] = session
        return session

    def get_session(self, session_id):
        return self.sessions.get(session_id)

    def get_all_sessions(self):
        return self.sessions

    def remove_session(self, session_id):
        session = self.sessions.pop(session_id, None)
        if session:
            session.close_session()

    def get_session_by_ip(self, attacker_ip):
        for session in self.sessions.values():
            if session.get_session()["attacker_ip"] == attacker_ip:
                return session
        return None

    def get_or_create_session(self, attacker_ip):
        session = self.get_session_by_ip(attacker_ip)
        if session is None:
            session = self.create_session(attacker_ip)
        return session
