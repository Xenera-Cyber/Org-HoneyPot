import datetime
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

# ==========================================
# EXPANSION PACK HELPER FUNCTIONS
# ==========================================
def handle_date(command):
    now = datetime.datetime.now()
    return now.strftime("%a %b %d %H:%M:%S UTC %Y")

def handle_env(command):
    return """SHELL=/bin/bash
PWD=/root
LOGNAME=root
HOME=/root
LANG=en_US.UTF-8
LS_COLORS=rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:
LESSCLOSE=/usr/bin/lesspipe %s %s
TERM=xterm-256color
LESSOPEN=| /usr/bin/lesspipe %s
USER=root
SHLVL=1
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
_=/usr/bin/env"""

def handle_printenv(command):
    return handle_env(command)

def handle_echo(command):
    parts = command.split(" ", 1)
    if len(parts) > 1:
        return parts[1].strip("\"'") 
    return ""

def handle_clear(command):
    return "\033[2J\033[H"

def handle_which(command):
    parts = command.split()
    if len(parts) < 2:
        return ""
    target = parts[1]
    common_bins = ["ls", "cat", "wget", "curl", "python", "python3", "bash", "sh", "chmod", "chown", "rm", "cp", "mv", "scp", "whoami"]
    if target in common_bins:
        return f"/usr/bin/{target}"
    return ""

def handle_who(command):
    return "root     pts/0        2026-06-29 10:14 (192.168.1.45)"

def handle_w(command):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    return f""" {now} up 14 days,  3:12,  1 user,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
root     pts/0    192.168.1.45     10:14    1.00s  0.02s  0.00s -bash"""

def handle_alias(command):
    return """alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'
alias grep='grep --color=auto'
alias l='ls -CF'
alias la='ls -A'
alias ll='ls -alF'
alias ls='ls --color=auto'"""

def handle_hostnamectl(command):
    return """   Static hostname: xynera-server
         Icon name: computer-vm
           Chassis: vm
        Machine ID: 8a4e8d3a5b6c4f729e1f2d3c4b5a6978
           Boot ID: 1b2c3d4f5a6b7c8d9e0f1a2b3c4d5e6f
    Virtualization: kvm
  Operating System: Ubuntu 22.04.3 LTS
            Kernel: Linux 5.15.0-82-generic
      Architecture: x86-64"""

def handle_history(command, session_manager):
    session = session_manager.get_session()
    # Safely fetch history, defaulting to a basic list if it doesn't exist yet
    history = session.get("history", ["cd /", "ls -la", "pwd", command])
    output = ""
    for i, cmd in enumerate(history, 1):
        output += f"  {i}  {cmd}\n"
    return output.strip()


# ==========================================
# MAIN ROUTER LOGIC
# ==========================================
def route_command(command, session_manager):
    session = session_manager.get_session()
    cwd = session["cwd"]
    command = command.strip()

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
    # NEW EXPANSION PACK COMMANDS
    # --------------------------
    elif command.startswith("date"):
        return handle_date(command)

    elif command.startswith("env"):
        return handle_env(command)

    elif command.startswith("printenv"):
        return handle_printenv(command)

    elif command.startswith("echo"):
        return handle_echo(command)

    elif command.startswith("clear"):
        return handle_clear(command)

    elif command.startswith("which"):
        return handle_which(command)

    elif command.startswith("who"):
        return handle_who(command)

    elif command.startswith("w"):
        return handle_w(command)

    elif command.startswith("alias"):
        return handle_alias(command)

    elif command.startswith("hostnamectl"):
        return handle_hostnamectl(command)

    elif command.startswith("history"):
        return handle_history(command, session_manager)

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