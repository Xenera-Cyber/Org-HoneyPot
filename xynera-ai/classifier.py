def classify_command(command: str) -> str:

    cmd = command.lower()

    if "nmap" in cmd:
        return "Reconnaissance"

    elif "wget" in cmd or "curl" in cmd:
        return "Malware Download Attempt"

    elif "chmod" in cmd:
        return "Permission Manipulation"

    elif "nc" in cmd or "netcat" in cmd:
        return "Reverse Shell Attempt"

    else:
        return "Unknown"
