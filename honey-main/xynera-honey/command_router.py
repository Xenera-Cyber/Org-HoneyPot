from fake_filesystem import filesystem, file_contents
from fake_process import ps, ps_aux
from fake_network import (
    netstat,
    netstat_tulpn,
    ss,
    ifconfig,
    ip_addr,
)
import malware_detector
import deception_engine
import ai_client

def route_command(command, session_manager, attack_type=None):
    session = session_manager.get_session()
    cwd = session["cwd"]
    command = command.strip()

    if attack_type is None:
        from attack_analyzer import classify
        attack_type = classify(command)

    # --------------------------
    # USER COMMANDS
    # --------------------------
    if command == "whoami":
        return "ubuntu"

    elif command == "groups":
        return "ubuntu sudo docker"

    elif command == "id":
        return (
            "uid=1000(ubuntu) "
            "gid=1000(ubuntu) "
            "groups=1000(ubuntu)"
        )

    elif command == "users":
        return "ubuntu"

    # --------------------------
    # DIRECTORY COMMANDS
    # --------------------------
    elif command == "pwd":
        return cwd

    elif command == "ls":
        return "\n".join(filesystem.get(cwd, []))

    elif command == "ls -la":
        files = filesystem.get(cwd, [])
        return "\n".join(
            f"-rw-r--r-- 1 ubuntu ubuntu 1024 Jun 25 {f}"
            for f in files
        )

    # --------------------------
    # CHANGE DIRECTORY
    # --------------------------
    elif command.startswith("cd "):
        path = command[3:].strip()

        if path == "..":
            if cwd != "/":
                parent = "/".join(cwd.rstrip("/").split("/")[:-1])
                session_manager.change_directory(parent if parent else "/")
            return ""

        new_path = path if path.startswith("/") else (
            f"/{path}" if cwd == "/" else f"{cwd}/{path}"
        )
        new_path = new_path.replace("//", "/")

        if new_path in filesystem:
            session_manager.change_directory(new_path)
            return ""

    # --------------------------
    # FILE COMMANDS
    # --------------------------
    elif command.startswith("cat "):
        filename = command[4:].strip()
        full_path = filename if filename.startswith("/") else f"{cwd}/{filename}"
        full_path = full_path.replace("//", "/")

        if full_path == "/etc/hostname":
            return (hostname if hostname else "ubuntu-server") + "\n"

        if full_path in file_contents:
            return file_contents[full_path]

    # --------------------------
    # PROCESS COMMANDS
    # --------------------------
    elif command == "ps":
        return ps()

    elif command == "ps aux":
        return ps_aux()

    # --------------------------
    # NETWORK COMMANDS
    # --------------------------
    elif command == "netstat":
        return netstat()

    elif command == "netstat -tulpn":
        return netstat_tulpn()

    elif command == "ss":
        return ss()

    elif command == "ifconfig":
        return ifconfig()

    elif command == "ip addr":
        return ip_addr()

    # --------------------------
    # SYSTEM DISCOVERY
    # --------------------------
    elif command == "hostname":
        return "web-prod-01"

    elif command == "uname -a":
        return "Linux web-prod-01 5.15.0-generic x86_64 GNU/Linux"

    elif command == "uptime":
        return "14:23:05 up 37 days, 3 users, load average: 0.11, 0.09, 0.05"

    elif command == "systemctl":
        return """ssh.service active
nginx.service active
mysql.service active
redis.service active"""

    # --------------------------
    # DECEPTION ENGINE & AI BACKEND ROUTING
    # --------------------------
    history = [c["command"] for c in session.get("command_history", [])]

    # Try Deception Engine overrides first
    deception_resp = deception_engine.adapt_response(command, session, attack_type)
    if deception_resp is not None:
        return deception_resp

    # Try AI Backend for adaptive, contextual simulation
    hostname = "web-prod-01"
    username = "ubuntu"

    ai_resp = ai_client.send_to_ai(
        ip=session.get("attacker_ip", "UNKNOWN"),
        command=command,
        history=history,
        attack_type=attack_type,
        cwd=cwd,
        hostname=hostname,
        username=username
    )
    if ai_resp is not None:
        return ai_resp

    # --------------------------
    # LOCAL FALLBACKS
    # --------------------------
    if command.startswith("cd "):
        path = command[3:].strip()
        return f"cd: no such file or directory: {path}"

    elif command.startswith("cat "):
        filename = command[4:].strip()
        return f"cat: {filename}: No such file"

    elif command.startswith("wget"):
        return malware_detector.handle_wget(command)[0]

    elif command.startswith("curl"):
        return malware_detector.handle_curl(command)[0]

    elif command.startswith("scp"):
        return malware_detector.handle_scp(command)[0]

    elif command.startswith("chmod"):
        return "Permissions updated"

    elif command.startswith("nc"):
        return "Connection established"

    # --------------------------
    # DEFAULT
    # --------------------------
    return f"{command}: command not found"
