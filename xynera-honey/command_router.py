import time
import random
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
# --------------------------
# Delay Configuration
# --------------------------

ENABLE_RANDOM_DELAY = True
DELAY_VARIATION = 0.15

COMMAND_DELAYS = {
    "default": 0.2,

    "whoami": 0.2,
    "groups": 0.2,
    "id": 0.2,
    "users": 0.2,

    "pwd": 0.2,
    "ls": 0.2,
    "ls -la": 0.3,
    "cd": 0.2,
    "cat": 0.4,

    "ps": 0.5,
    "ps aux": 0.7,

    "netstat": 0.8,
    "netstat -tulpn": 1.0,
    "ss": 0.8,
    "ifconfig": 0.8,
    "ip addr": 0.8,

    "hostname": 0.2,
    "uname -a": 0.3,
    "uptime": 0.3,
    "systemctl": 0.7,

    "wget": 2.0,
    "curl": 2.0,
    "scp": 2.0,
    "chmod": 0.3,
    "nc": 1.5,
}



def get_command_delay(command):
    command = command.strip()

    if not command:
        return COMMAND_DELAYS["default"]

    base_command = command.split()[0]

    base_delay = COMMAND_DELAYS.get(
        command,
        COMMAND_DELAYS.get(
            base_command,
            COMMAND_DELAYS["default"]
        )
    )

    if ENABLE_RANDOM_DELAY:
     variation = base_delay * DELAY_VARIATION
     random_delay = random.uniform(-variation, variation)
     return max(0, base_delay + random_delay)

    return base_delay



def route_command(command, session_manager):
    session = session_manager.get_session()
    cwd = session["cwd"]
    command = command.strip()

    time.sleep(get_command_delay(command))

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

        return f"cd: no such file or directory: {path}"

    # --------------------------
    # FILE COMMANDS
    # --------------------------
    elif command.startswith("cat "):
        filename = command[4:].strip()
        full_path = filename if filename.startswith("/") else f"{cwd}/{filename}"
        full_path = full_path.replace("//", "/")

        if full_path in file_contents:
            return file_contents[full_path]

        return f"cat: {filename}: No such file"

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
    # ATTACKER COMMANDS
    # --------------------------
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
