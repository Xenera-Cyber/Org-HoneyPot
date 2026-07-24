"""
session_manager.py

Unified session management for honeypot sessions, incorporating per-session state,
identity/filesystem synchronization, dynamic prompt generation, backend caches,
and centralized cache tracking via CacheManager.
"""

import uuid
import json
import os
from datetime import datetime
from posixpath import dirname, basename
from typing import Dict, Any, Optional, List, Tuple

from fake_filesystem import create_filesystem, SYSTEM_USERS, DEFAULT_OWNER, DEFAULT_GROUP
from service_manager import ServiceManager
from cache_manager import get_cache_manager

HOME_DIR = "/home/ubuntu"
DEFAULT_HOSTNAME = "web-prod-01"
DEFAULT_USERNAME = "ubuntu"
DEFAULT_GROUPS = ["ubuntu", "sudo", "docker"]
DEFAULT_KERNEL = "5.15.0-82-generic"
DEFAULT_SHELL = "/bin/bash"

DEFAULT_PERSONALITY = {
    "name": "Standard Ubuntu Server",
    "hostname": DEFAULT_HOSTNAME,
    "user": DEFAULT_USERNAME,
    "groups": DEFAULT_GROUPS,
    "home_dir": HOME_DIR,
    "shell": DEFAULT_SHELL,
}


class SessionManager:
    """Enhanced session manager with dynamic identity synchronization"""
    
    def __init__(self, attacker_ip: str):
        self.session_id = str(uuid.uuid4())
        self.attacker_ip = attacker_ip
        
        # Per-session dynamic filesystem
        self.filesystem = create_filesystem(session_id=self.session_id)
        self.services = ServiceManager()
        self._cache = get_cache_manager()
        
        # Backend-facing caches: per-session storage for anything the AI
        # backend supplies (dynamic file content, precomputed command
        # responses, identity snapshots, service snapshots).
        self.backend_cache = {
            "filesystem": {},
            "responses": {},
            "identity": {},
            "services": {},
            "metadata": {
                "attacker_ip": attacker_ip,
            },
        }
        
        # Dynamic per-attacker hostname: derived from attacker's IP
        dynamic_hostname = (
            f"node-{attacker_ip.split('.')[-1]}" if attacker_ip and attacker_ip != "unknown" else DEFAULT_HOSTNAME
        )
        
        self.session = {
            "session_id": self.session_id,
            "attacker_ip": attacker_ip,
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "cwd": HOME_DIR,
            "command_history": [],
            "attack_types": [],
            "threat_score": 0,
            "is_active": True,
            "attacker_profile": {"intent": "recon"},
            
            # Identity parameters
            "username": DEFAULT_USERNAME,
            "hostname": dynamic_hostname,
            "groups": list(DEFAULT_GROUPS),
            "home_dir": HOME_DIR,
            "shell": DEFAULT_SHELL,
            "kernel_version": DEFAULT_KERNEL,
            "environment": {},
            "service_manager": self.services,
            "personality": None,
        }
        
        # Initialize identity synchronization
        self._initialize_identity()
    
    # ==========================================================
    # Initialization
    # ==========================================================
    
    def _initialize_identity(self):
        """Initialize all identity-related components"""
        self._sync_environment()
        self._sync_all_identity_files()
        self._apply_ownership(self.session["home_dir"], self.session["username"], self.session["groups"][0])
        self._sync_identity_cache()
        self.sync_service_state()
        self._update_session_cache()
    
    # ==========================================================
    # Attribute-style compatibility shims
    # ==========================================================
    
    @property
    def username(self) -> str:
        return self.session["username"]
    
    @property
    def hostname(self) -> str:
        return self.session["hostname"]
    
    @property
    def home_dir(self) -> str:
        return self.session["home_dir"]
    
    @property
    def groups(self) -> List[str]:
        return self.session["groups"]
    
    @property
    def kernel_version(self) -> str:
        return self.session["kernel_version"]
    
    @property
    def environment(self) -> Dict[str, str]:
        return self.session["environment"]
    
    @property
    def service_manager(self) -> ServiceManager:
        return self.services
    
    # ==========================================================
    # Cache Helpers
    # ==========================================================
    
    def _update_session_cache(self):
        """Update session state in CacheManager"""
        self._cache.set(
            f"session:{self.session_id}",
            self.session,
            ttl=3600,
            dependencies=[f"session:{self.session_id}"]
        )
    
    def get_session(self) -> Dict:
        return self.session
    
    def get_cwd(self) -> str:
        return self.session["cwd"]
    
    def get_hostname(self) -> str:
        return self.session["hostname"]
    
    def get_username(self) -> str:
        return self.session["username"]
    
    def get_environment(self) -> Dict[str, str]:
        return self.session["environment"]
    
    def get_filesystem(self):
        return self.filesystem
    
    def get_services(self):
        return self.services
    
    def get_prompt(self) -> str:
        """Get the shell prompt string."""
        home = self.session["home_dir"]
        cwd = self.session["cwd"]
        if cwd == home:
            display_path = "~"
        elif cwd.startswith(home + "/"):
            display_path = cwd.replace(home, "~", 1)
        else:
            display_path = cwd
        return f"{self.session['username']}@{self.session['hostname']}:{display_path}$ "
    
    def get_ps1(self) -> str:
        """Alias for get_prompt() - PS1 environment variable format"""
        return self.get_prompt()
    
    def change_directory(self, path: str):
        """Change current directory with identity sync"""
        self.session["cwd"] = path
        self.session["environment"]["PWD"] = path
        self.backend_cache["metadata"]["cwd"] = path
        self._update_session_cache()
    
    def add_command(self, command: str):
        """Add command to history with identity sync"""
        self.session["command_history"].append({
            "command": command,
            "timestamp": datetime.now().isoformat(),
            "cwd": self.session["cwd"]
        })
        # Invalidate command-related cache
        self._cache.invalidate_dependent(f"commands:{self.session_id}")
        self._update_session_cache()
    
    def add_attack_type(self, attack_type: str):
        if attack_type not in self.session["attack_types"]:
            self.session["attack_types"].append(attack_type)
            self._update_session_cache()
    
    def update_threat_score(self, score: int):
        self.session["threat_score"] += score
        self._update_session_cache()
    
    def update_personality(self, personality_name: Optional[str] = None):
        if personality_name:
            self.session["personality"] = personality_name
            self._update_session_cache()
    
    # ==========================================================
    # Backend cache management
    # ==========================================================
    
    def sync_service_state(self):
        """Sync service states to backend cache"""
        self.backend_cache["services"] = {
            name: dict(info)
            for name, info in self.services.services.items()
        }
    
    def sync_backend_after_filesystem_write(self):
        self.invalidate_backend()
    
    def backend_exists(self, path: str) -> bool:
        return path in self.backend_cache["filesystem"]
    
    def get_backend(self, path: str, default=None):
        return self.backend_cache["filesystem"].get(path, default)
    
    def save_backend(self, path: str, data):
        self.backend_cache["filesystem"][path] = data
        return data
    
    def preload_backend(self, path: str, content):
        self.invalidate_backend(path)
        return self.save_backend(path, content)
    
    def invalidate_backend(self, path: Optional[str] = None):
        if path is None:
            self.backend_cache["filesystem"].clear()
            return
        self.backend_cache["filesystem"].pop(path, None)
    
    def response_exists(self, command: str) -> bool:
        return command in self.backend_cache["responses"]
    
    def get_response(self, command: str, default=None):
        return self.backend_cache["responses"].get(command, default)
    
    def save_response(self, command: str, response):
        self.backend_cache["responses"][command] = response
        return response
    
    def _sync_identity_cache(self):
        """Sync identity to backend cache"""
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
    
    # ==========================================================
    # CORE: Dynamic Identity Synchronization
    # ==========================================================
    
    def _sync_environment(self):
        """Synchronize environment variables with current identity"""
        self.session["environment"] = {
            "SHELL": self.session["shell"],
            "PWD": self.session["cwd"],
            "LOGNAME": self.session["username"],
            "HOME": self.session["home_dir"],
            "LANG": "en_US.UTF-8",
            "TERM": "xterm-256color",
            "USER": self.session["username"],
            "HOSTNAME": self.session["hostname"],
            "SHLVL": "1",
            "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
            "_": "/usr/bin/env",
            "OLDPWD": self.session["home_dir"],
        }
    
    def _sync_all_identity_files(self):
        """Synchronize all identity-related files (/etc/passwd, /etc/hostname, /etc/hosts)"""
        # Always write hostname with current value
        self._write_file("/etc/hostname", f"{self.session['hostname']}\n")
        # Always render hosts with current hostname
        self._write_file("/etc/hosts", self._render_hosts())
        # Update passwd
        self._write_file("/etc/passwd", self._render_passwd())
        
        # Invalidate backend cache for identity files
        self.invalidate_backend("/etc/hostname")
        self.invalidate_backend("/etc/hosts")
        self.invalidate_backend("/etc/passwd")
        
        # Also invalidate filesystem cache
        self.filesystem._cache.invalidate_dependent("/etc/hostname")
        self.filesystem._cache.invalidate_dependent("/etc/hosts")
        self.filesystem._cache.invalidate_dependent("/etc/passwd")
    
    def _render_hosts(self) -> str:
        """Render /etc/hosts with current session hostname"""
        current_hostname = self.session["hostname"]
        
        # Build hosts file with current hostname
        hosts_lines = [
            "127.0.0.1 localhost",
            f"127.0.1.1 {current_hostname}",
            "10.0.0.10 db-prod-01",
            "10.0.0.11 backup-01"
        ]
        
        return "\n".join(hosts_lines) + "\n"
    
    def _render_passwd(self) -> str:
        """Render /etc/passwd with current session username"""
        # Get existing passwd content or use default
        existing = self.filesystem.cat("/", "/etc/passwd")
        if existing.startswith("cat:"):
            existing = "root:x:0:0:root:/root:/bin/bash\n"
        
        username = self.session["username"]
        home_dir = self.session["home_dir"]
        shell = self.session["shell"]
        
        # Get or create user entry
        if username in SYSTEM_USERS:
            user = SYSTEM_USERS[username]
            uid = user["uid"]
            gid = user["gid"]
            full_name = username.title()
        else:
            # Dynamic user - assign next available UID
            uid = 2000
            gid = 2000
            full_name = username.title()
        
        replacement = f"{username}:x:{uid}:{gid}:{full_name}:{home_dir}:{shell}"
        
        # Process existing passwd lines
        lines = []
        replaced = False
        for line in existing.splitlines():
            if not line:
                continue
            account = line.split(":", 1)[0]
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
    
    def _write_file(self, path: str, content: str):
        """Write content to a file with proper handling"""
        # Ensure parent directory exists
        parent_path = dirname(path)
        if parent_path != "/" and not self.filesystem.exists(parent_path):
            self._ensure_parent_dirs(parent_path)
        
        # Create or update file
        filename = basename(path)
        parent_dir = dirname(path)
        
        if not self.filesystem.exists(path):
            # Use the correct cwd for touch
            if parent_dir == "/":
                self.filesystem.touch("/", filename)
            else:
                self.filesystem.touch(parent_dir, filename)
        
        # Update the content
        node = self.filesystem.get_node(path)
        if node is not None and hasattr(node, "content"):
            node.content = content
            node.metadata.touch()
            # Invalidate cache for this file
            self._cache.invalidate_dependent(path)
            self.filesystem._invalidate_path(path)
    
    def _ensure_parent_dirs(self, path: str):
        """Ensure all parent directories exist"""
        if path == "/" or path == "":
            return
        if not self.filesystem.exists(path):
            parent = dirname(path)
            self._ensure_parent_dirs(parent)
            # Create this directory
            if parent == "/":
                self.filesystem.mkdir("/", path.lstrip("/"))
            else:
                self.filesystem.mkdir(parent, basename(path))
    
    def _apply_ownership(self, path: str, owner: str, group: str):
        """Apply ownership recursively"""
        node = self.filesystem.get_node(path)
        if node is None:
            return
        node.owner = owner
        node.group = group
        if hasattr(node, "children"):
            for child in node.children.values():
                self._apply_ownership(child.path(), owner, group)
    
    # ==========================================================
    # IDENTITY MANAGEMENT API
    # ==========================================================
    
    def set_username(self, username: str) -> bool:
        """
        Change the session username.
        Updates: /etc/passwd, environment, prompt, ownership
        """
        if not username or not username.isalnum():
            return False
        
        old_username = self.session["username"]
        old_home = self.session["home_dir"]
        
        # Update session
        self.session["username"] = username
        self.session["home_dir"] = f"/home/{username}"
        
        # Sync environment
        self._sync_environment()
        
        # Sync all identity files (passwd, hostname, hosts)
        self._sync_all_identity_files()
        
        # Update ownership of home directory if it exists
        if self.filesystem.exists(old_home):
            # Rename home directory
            self.filesystem.mv("/", old_home.lstrip("/"), self.session["home_dir"].lstrip("/"))
            self._apply_ownership(self.session["home_dir"], username, username)
        
        # Update cache
        self._sync_identity_cache()
        self._update_session_cache()
        
        print(f"[+] Username changed from {old_username} to {username}")
        return True
    
    def set_hostname(self, hostname: str) -> bool:
        """
        Change the session hostname.
        Updates: /etc/hostname, /etc/hosts, environment, prompt
        """
        if not hostname or not hostname.replace("-", "").replace("_", "").isalnum():
            return False
        
        old_hostname = self.session["hostname"]
        self.session["hostname"] = hostname
        
        # Update environment
        self.session["environment"]["HOSTNAME"] = hostname
        
        # Update files - force write
        self._write_file("/etc/hostname", f"{hostname}\n")
        self._write_file("/etc/hosts", self._render_hosts())
        
        # Update cache
        self._sync_identity_cache()
        self._update_session_cache()
        
        print(f"[+] Hostname changed from {old_hostname} to {hostname}")
        return True
    
    def set_identity(self, username: Optional[str] = None, hostname: Optional[str] = None, personality: Optional[str] = None):
        """Set multiple identity parameters at once"""
        old_username = self.session["username"]
        
        if username:
            self.session["username"] = username
        if hostname:
            self.session["hostname"] = hostname
        if personality:
            self.session["personality"] = personality
        
        if username or hostname:
            self._sync_environment()
            self._sync_all_identity_files()
            self._apply_ownership(
                self.session["home_dir"], self.session["username"], self.session["groups"][0]
            )
        self._sync_identity_cache()
        self._update_session_cache()
    
    def get_identity(self) -> Dict:
        """Get current identity snapshot"""
        return {
            "username": self.session["username"],
            "hostname": self.session["hostname"],
            "home_dir": self.session["home_dir"],
            "shell": self.session["shell"],
            "groups": self.session["groups"],
            "kernel_version": self.session["kernel_version"],
            "personality": self.session["personality"],
            "cwd": self.session["cwd"],
        }
    
    # ==========================================================
    # LIFECYCLE METHODS
    # ==========================================================
    
    def close_session(self):
        """Close and export session"""
        if not self.session["is_active"]:
            return
        
        self.session["is_active"] = False
        self.session["end_time"] = datetime.now().isoformat()
        self.export_session()
        
        # Clear session cache
        self._cache.invalidate(f"session:{self.session_id}")
    
    def export_session(self):
        """Export session to JSON"""
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
            "hostname": self.session["hostname"],
            "username": self.session["username"],
            "groups": self.session["groups"],
            "personality": self.session["personality"],
            "environment": self.session["environment"],
        }
        
        filename = f"{log_dir}/session_{self.session['session_id']}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(session_data, f, indent=4)
        
        print(f"[+] Session exported -> {filename}")
    
    def summary(self) -> Dict:
        """Get session summary"""
        return {
            "session_id": self.session["session_id"],
            "attacker_ip": self.session["attacker_ip"],
            "hostname": self.session["hostname"],
            "username": self.session["username"],
            "home_dir": self.session["home_dir"],
            "current_directory": self.session["cwd"],
            "commands_executed": len(self.session["command_history"]),
            "attack_types": self.session["attack_types"],
            "threat_score": self.session["threat_score"],
            "is_active": self.session["is_active"],
            "personality": self.session["personality"],
        }
    
    # ==========================================================
    # Consistency Verification (for testing)
    # ==========================================================
    
    def verify_consistency(self) -> Dict:
        """Verify filesystem and session consistency."""
        issues = []
        
        # Check filesystem consistency
        fs_consistency = self.filesystem.verify_consistency()
        if not fs_consistency["consistent"]:
            issues.extend(fs_consistency["issues"])
        
        # Check /etc/passwd matches session username
        passwd_file = self.filesystem.cat("/", "/etc/passwd")
        if f"{self.session['username']}:x:" not in passwd_file:
            issues.append(f"User {self.session['username']} not found in /etc/passwd")
        
        # Check environment consistency
        if self.session["environment"].get("USER") != self.session["username"]:
            issues.append(f"USER environment mismatch: {self.session['environment'].get('USER')} != {self.session['username']}")
        
        if self.session["environment"].get("HOSTNAME") != self.session["hostname"]:
            issues.append(f"HOSTNAME environment mismatch: {self.session['environment'].get('HOSTNAME')} != {self.session['hostname']}")
        
        if self.session["environment"].get("HOME") != self.session["home_dir"]:
            issues.append(f"HOME environment mismatch: {self.session['environment'].get('HOME')} != {self.session['home_dir']}")
        
        if self.session["environment"].get("PWD") != self.session["cwd"]:
            issues.append(f"PWD environment mismatch: {self.session['environment'].get('PWD')} != {self.session['cwd']}")
        
        # Check /etc/hosts contains hostname
        hosts_file = self.filesystem.cat("/", "/etc/hosts")
        if self.session["hostname"] not in hosts_file:
            issues.append(f"Hostname '{self.session['hostname']}' not found in /etc/hosts")
        
        # Check cache sync
        cached_session = self._cache.get(f"session:{self.session_id}")
        if not cached_session:
            issues.append("Session not found in cache")
        
        return {
            "consistent": len(issues) == 0,
            "issues": issues,
            "fs_consistency": fs_consistency,
            "session_data": self.summary()
        }
    
    def verify_identity_sync(self) -> Dict:
        """Verify all identity components are synchronized"""
        issues = []
        
        # Check /etc/hostname
        hostname_file = self.filesystem.cat("/", "/etc/hostname").strip()
        if hostname_file != self.session["hostname"]:
            issues.append(f"Hostname mismatch: /etc/hostname='{hostname_file}', session='{self.session['hostname']}'")
        
        # Check /etc/hosts contains hostname
        hosts_file = self.filesystem.cat("/", "/etc/hosts")
        if self.session["hostname"] not in hosts_file:
            issues.append(f"Hostname '{self.session['hostname']}' not found in /etc/hosts")
        
        # Check /etc/passwd contains username
        passwd_file = self.filesystem.cat("/", "/etc/passwd")
        if f"{self.session['username']}:x:" not in passwd_file:
            issues.append(f"Username '{self.session['username']}' not found in /etc/passwd")
        
        # Check environment
        if self.session["environment"].get("USER") != self.session["username"]:
            issues.append(f"USER environment mismatch: {self.session['environment'].get('USER')} != {self.session['username']}")
        
        if self.session["environment"].get("HOSTNAME") != self.session["hostname"]:
            issues.append(f"HOSTNAME environment mismatch: {self.session['environment'].get('HOSTNAME')} != {self.session['hostname']}")
        
        return {
            "synchronized": len(issues) == 0,
            "issues": issues,
            "identity": self.get_identity(),
            "environment": self.session["environment"],
            "prompt": self.get_prompt(),
        }


# ==========================================================
# Multi-Client Session Handling
# ==========================================================

class MultiSessionManager:
    """Track multiple concurrent sessions"""
    
    def __init__(self):
        self.sessions: Dict[str, SessionManager] = {}
    
    def create_session(self, attacker_ip: str) -> SessionManager:
        session = SessionManager(attacker_ip)
        self.sessions[session.session_id] = session
        return session
    
    def get_session(self, session_id: str) -> Optional[SessionManager]:
        return self.sessions.get(session_id)
    
    def get_all_sessions(self) -> Dict[str, SessionManager]:
        return self.sessions
    
    def remove_session(self, session_id: str):
        session = self.sessions.pop(session_id, None)
        if session:
            session.close_session()
    
    def get_session_by_ip(self, attacker_ip: str) -> Optional[SessionManager]:
        for session in self.sessions.values():
            if session.session["attacker_ip"] == attacker_ip:
                return session
        return None
    
    def get_or_create_session(self, attacker_ip: str) -> SessionManager:
        session = self.get_session_by_ip(attacker_ip)
        if session is None:
            session = self.create_session(attacker_ip)
        return session
    
    def get_active_count(self) -> int:
        return len([s for s in self.sessions.values() if s.session["is_active"]])