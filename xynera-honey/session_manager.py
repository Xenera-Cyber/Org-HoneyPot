import uuid
import json
import os
from datetime import datetime

HOME_DIR = "/home/ubuntu"


class SessionManager:
    def __init__(self, attacker_ip):
        self.session = {
            "session_id": str(uuid.uuid4()),
            "attacker_ip": attacker_ip,
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "cwd": HOME_DIR,
            "command_history": [],
            "attack_types": [],
            "threat_score": 0,
            "is_active": True
        }

    def get_session(self):
        return self.session

    def get_cwd(self):
        return self.session["cwd"]

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
            "session_duration": duration
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
            "is_active": self.session["is_active"]
        }