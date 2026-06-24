def classify(command):
    cmd = command.lower()

    if "nmap" in cmd:
        return "Reconnaissance"

    elif "wget" in cmd or "curl" in cmd:
        return "Malware Download"

    elif "/etc/passwd" in cmd:
        return "Privilege Enumeration"

    elif "ssh" in cmd:
        return "Lateral Movement"

    return "Unknown"
