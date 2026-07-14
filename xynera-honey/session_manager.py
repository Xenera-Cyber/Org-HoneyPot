import uuid
import json
import os
from datetime import datetime

from fake_filesystem import create_filesystem
from service_manager import ServiceManager

HOME_DIR = "/home/ubuntu"


class SessionManager:
    def __init__(self, attacker_ip):
        # Per-session dynamic filesystem (touch/mkdir/rm/mv/cp persist for
        # the life of this session only, never leaking into other sessions).
        self.filesystem = create_filesystem()

        # Per-session fake service state (nginx/mysql/redis/ssh/docker),
        # so `service <n> stop`, `systemctl status <n>`, `netstat`, and
        # `ss` all agree with each other for this attacker.
        self.services = ServiceManager()

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
            # outside this class should ever hardcode a username, hostname
            # or prompt string. Everything must read it from here via
            # get_prompt() / get_identity(), so that when the AI backend
            # (or anything else) changes the identity mid-session, every
            # future prompt automatically reflects it.
            # ------------------------------------------------------------
            "username": "ubuntu",
            "hostname": "web-prod-01",
            "personality": "default",
        }

    def get_session(self):
        return self.session

    def get_cwd(self):
        return self.session["cwd"]

    def get_filesystem(self):
        return self.filesystem

    def get_services(self):
        return self.services

    def change_directory(self, path):
        self.session["cwd"] = path

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
    # SESSION IDENTITY -- new
    # ------------------------------------------------------------------
    def set_identity(self, username=None, hostname=None, personality=None):
        """
        Called whenever the identity needs to change (e.g. the AI backend
        decides this session should now look like a different machine/user).
        Only updates the fields that are actually passed in; anything left
        as None stays unchanged.
        """
        if username:
            self.session["username"] = username
        if hostname:
            self.session["hostname"] = hostname
        if personality:
            self.session["personality"] = personality

    def get_identity(self):
        return {
            "username": self.session["username"],
            "hostname": self.session["hostname"],
            "personality": self.session["personality"],
            "cwd": self.session["cwd"],
        }

    def get_prompt(self):
        """
        Builds the shell prompt LIVE from current session state.
        This is the ONLY function that should ever be used to generate
        the prompt string anywhere in the codebase -- never hardcode
        "username@hostname:cwd$" again. Whatever set_identity() last set
        is what will show up here, automatically.
        """
        cwd = self.session["cwd"]
        if cwd == HOME_DIR:
            display_path = "~"
        elif cwd.startswith(HOME_DIR):
            display_path = cwd.replace(HOME_DIR, "~", 1)
        else:
            display_path = cwd
        return f"{self.session['username']}@{self.session['hostname']}:{display_path}$ "

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
            # identity is now part of the permanent record too, so if it
            # changed mid-session, that's visible in the logs afterwards
            "username": self.session["username"],
            "hostname": self.session["hostname"],
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
            "current_directory": self.session["cwd"],
            "commands_executed": len(
                self.session["command_history"]
            ),
            "attack_types": self.session["attack_types"],
            "threat_score": self.session["threat_score"],
            "is_active": self.session["is_active"],
            "username": self.session["username"],
            "hostname": self.session["hostname"],
            "personality": self.session["personality"],
        }