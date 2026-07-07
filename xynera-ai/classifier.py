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

    elif "sqlmap" in cmd:
        return "SQL Injection Attempt"

    elif "history -c" in cmd or "rm -rf /var/log" in cmd or "stop auditd" in cmd:
        return "Defense Evasion"

    elif "authorized_keys" in cmd or "useradd" in cmd or "cron" in cmd:
        return "Persistence Creation"

    elif "find / -perm" in cmd or "pkexec" in cmd or "dirtycow" in cmd:
        return "Privilege Escalation Attempt"

    elif any(ind in cmd for ind in ["xmrig", "minerd", "mirai", "mozi", "tsunami", "base64 -d", "./tmp", "./dev/shm", "/tmp/"]):
        return "Malware Execution Attempt"

    else:
        return "Unknown"
