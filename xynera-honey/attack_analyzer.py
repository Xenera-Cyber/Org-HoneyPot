SHARED_ATTACK_SCORES = {
    "Reconnaissance": 20,
    "Directory Navigation": 10,
    "Credential Enumeration": 60,
    "Malware Download": 90,
    "Malware Preparation": 95,
    "Malware Execution": 100,
    "File Transfer": 80,
    "Privilege Escalation": 95,
    "Lateral Movement": 80,
    "Destructive Attack": 100,
    "Reverse Shell Activity": 100,
    "Unknown": 5,
}

def classify(command):
    cmd = command.lower().strip()

    # --------------------------
    # Reconnaissance
    # --------------------------
    if (
        cmd in [
            "ls", "pwd", "whoami", "id", "groups", "hostname", "users"
        ]
        or cmd.startswith("uname")
        or cmd.startswith("ifconfig")
        or cmd.startswith("ip ")
        or cmd.startswith("netstat")
        or cmd == "ss" or cmd.startswith("ss ")
        or cmd.startswith("ps")
        or any(tool in cmd for tool in [
            "nmap", "traceroute", "whois", "dig", "nslookup"
        ])
    ):
        return "Reconnaissance"

    # --------------------------
    # Directory Navigation
    # --------------------------
    elif cmd.startswith("cd"):
        return "Directory Navigation"

    # --------------------------
    # Credential Enumeration
    # --------------------------
    elif "/etc/passwd" in cmd or "/etc/shadow" in cmd:
        return "Credential Enumeration"

    # --------------------------
    # Malware Download
    # --------------------------
    elif "wget" in cmd or "curl" in cmd:
        return "Malware Download"

    # --------------------------
    # File Transfer
    # --------------------------
    elif cmd.startswith("scp"):
        return "File Transfer"

    # --------------------------
    # Privilege Escalation
    # --------------------------
    elif (
        "sudo" in cmd
        or "chmod" in cmd
        or cmd.startswith("su")
    ):
        return "Privilege Escalation"

    # --------------------------
    # Reverse Shell Activity
    # --------------------------
    elif (
        cmd.startswith("nc")
        or "bash -i" in cmd
        or "socket" in cmd
    ):
        return "Reverse Shell Activity"

    # --------------------------
    # Lateral Movement
    # --------------------------
    elif "ssh" in cmd:
        return "Lateral Movement"

    # --------------------------
    # Unknown
    # --------------------------
    return "Unknown"

def threat_score(attack_type):
    # This now accesses the master dictionary at the top of this file
    return SHARED_ATTACK_SCORES.get(attack_type, 5)