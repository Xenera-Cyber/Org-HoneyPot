def classify(command):

    cmd = command.lower()

    if any(tool in cmd for tool in [
        "nmap",
        "traceroute",
        "whois",
        "dig",
        "nslookup"
    ]):
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
