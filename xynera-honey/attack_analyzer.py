def classify(command):

    cmd = command.lower().strip()

    # Reconnaissance
    if (
        cmd == "ls" or
        cmd == "pwd" or
        cmd == "whoami" or
        cmd == "id" or
        cmd == "hostname" or
        cmd.startswith("uname") or
        cmd.startswith("ifconfig") or
        cmd.startswith("ip ") or
        cmd.startswith("netstat") or
        cmd.startswith("ss") or
        cmd.startswith("ps") or
        "nmap" in cmd
    ):
        return "Reconnaissance"

    # Directory Navigation
    elif cmd.startswith("cd"):
        return "Directory Navigation"

    # Credential Enumeration
    elif "/etc/passwd" in cmd or "/etc/shadow" in cmd:
        return "Credential Enumeration"

    # Malware Download
    elif "wget" in cmd or "curl" in cmd:
        return "Malware Download"

    # Privilege Escalation
    elif (
        "sudo" in cmd or
        "chmod" in cmd or
        cmd.startswith("su")
    ):
        return "Privilege Escalation"

    # Reverse Shell
    elif cmd.startswith("nc"):
        return "Reverse Shell Activity"

    # SSH / Lateral Movement
    elif "ssh" in cmd:
        return "Lateral Movement"

    return "Unknown"


def threat_score(attack_type):

    scores = {

        "Reconnaissance": 20,

        "Directory Navigation": 10,

        "Credential Enumeration": 60,

        "Malware Download": 90,

        "Privilege Escalation": 95,

        "Lateral Movement": 80,

        "Reverse Shell Activity": 100,

        "Unknown": 5

    }

    return scores.get(
        attack_type,
        5
    )