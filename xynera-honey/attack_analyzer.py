def classify(command):

    cmd = command.lower()

    if "nmap" in cmd:
        return "Reconnaissance"

    elif "wget" in cmd:
        return "Malware Download"

    elif "curl" in cmd:
        return "Malware Download"

    elif "/etc/passwd" in cmd:
        return "Privilege Enumeration"

    elif "ssh" in cmd:
        return "Lateral Movement"

    elif "chmod" in cmd:
        return "Privilege Escalation"

    elif cmd.startswith("nc"):
        return "Reverse Shell Activity"
   
    elif "bash -i" in cmd:
        return "Reverse Shell Activity"
   
    elif "netstat" in cmd:
        return "Reconnaissance"
   
    elif "socket" in cmd:
        return "Reverse Shell Activity"

    return "Unknown"


def threat_score(attack_type):

    scores = {

        "Reconnaissance": 1,

        "Privilege Enumeration": 3,

        "Malware Download": 5,

        "Privilege Escalation": 6,

        "Lateral Movement": 7,

        "Reverse Shell Activity": 10,

        "Unknown": 0
    }

    return scores.get(
        attack_type,
        0
    )
    
