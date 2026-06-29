import uuid
import json
import os
from datetime import datetime


class SessionManager:
    def __init__(self, attacker_ip):
        self.session = {
            "session_id": str(uuid.uuid4()),
            "attacker_ip": attacker_ip,
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "cwd": "/home/ubuntu",
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
        self.session["is_active"] = False
        self.session["end_time"] = datetime.now().isoformat()
        self.export_session()

    def export_session(self):
        os.makedirs("logs", exist_ok=True)

        start = datetime.fromisoformat(self.session["start_time"])
        end = datetime.fromisoformat(self.session["end_time"])

        duration = str(end - start)

        session_data = {
            "session_id": self.session["session_id"],
            "ip": self.session["attacker_ip"],
            "commands": self.session["command_history"],
            "threat_score": self.session["threat_score"],
            "attack_types": self.session["attack_types"],
            "session_duration": duration
        }

        filename = f"logs/session_{self.session['session_id']}.json"

        with open(filename, "w") as f:
            json.dump(session_data, f, indent=4)

        print(f"[+] Session exported -> {filename}")

    def summary(self):
        return {
            "session_id": self.session["session_id"],
            "attacker_ip": self.session["attacker_ip"],
            "commands_executed": len(self.session["command_history"]),
            "attack_types": self.session["attack_types"],
            "threat_score": self.session["threat_score"]
        }