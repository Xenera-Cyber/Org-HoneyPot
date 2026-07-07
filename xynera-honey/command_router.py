import time
import random
from datetime import datetime

from fake_filesystem import filesystem, file_contents
from fake_process import ps, ps_aux
from fake_network import (
    netstat,
    netstat_tulpn,
    ss,
    ifconfig,
    ip_addr,
    ssh,
    ping,
    traceroute,
    telnet,
    ftp,
    dig,
    nslookup,
    host,
)
import malware_detector

# ==========================================================
# Delay Configuration (configurable, never hardcoded)
# ==========================================================
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
    "ping": 1.0,
    "ssh": 1.5,
    "telnet": 1.0,
    "ftp": 1.0,
    "traceroute": 2.0,
    "dig": 0.5,
    "nslookup": 0.5,
    "host": 0.5,
    "hostname": 0.2,
    "hostnamectl": 0.3,
    "uname -a": 0.3,
    "uptime": 0.3,
    "systemctl": 0.7,
    "date": 0.1,
    "env": 0.1,
    "printenv": 0.1,
    "echo": 0.1,
    "clear": 0.1,
    "which": 0.1,
    "who": 0.1,
    "w": 0.1,
    "alias": 0.1,
    "history": 0.2,
    "wget": 2.0,
    "curl": 2.0,
    "scp": 2.0,
    "chmod": 0.3,
    "nc": 1.5,
}


def get_command_delay(command):
    """Look up a configurable, optionally randomized delay for a command."""
    command = command.strip()
    if not command:
        return COMMAND_DELAYS["default"]

    base_command = command.split()[0]
    base_delay = COMMAND_DELAYS.get(
        command,
        COMMAND_DELAYS.get(base_command, COMMAND_DELAYS["default"])
    )

    if ENABLE_RANDOM_DELAY:
        variation = base_delay * DELAY_VARIATION
        random_delay = random.uniform(-variation, variation)
        return max(0, base_delay + random_delay)

    return base_delay


# ==========================================================
# Expansion Pack Helper Functions
# ==========================================================
def handle_date(command):
    return datetime.now().strftime("%a %b %d %H:%M:%S UTC %Y")


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
    common_bins = [
        "ls", "cat", "wget", "curl", "python", "python3", "bash", "sh",
        "chmod", "chown", "rm", "cp", "mv", "scp", "whoami"
    ]
    if target in common_bins:
        return f"/usr/bin/{target}"
    return ""


def handle_who(command):
    return "root     pts/0        2026-06-29 10:14 (192.168.1.45)"


def handle_w(command):
    now = datetime.now().strftime("%H:%M:%S")
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
    """Render shell-style history from session["command_history"]."""
    session = session_manager.get_session()
    history = session.get("command_history", [])
    if not history:
        return ""
    return "\n".join(
        f"  {i}  {entry['command']}"
        for i, entry in enumerate(history, 1)
    )


# ==========================================================
# Network Command Helpers (shared arg-parsing, avoids duplication)
# ==========================================================
def _arg(command, index=1, default=None):
    parts = command.split()
    return parts[index] if len(parts) > index else default


def handle_ssh(command):
    parts = command.split()
    if len(parts) > 1 and "@" in parts[1]:
        user, target = parts[1].split("@", 1)
    else:
        user, target = "root", _arg(command, 1, "192.168.1.10")
    return ssh(host=target, user=user)


def handle_ping(command):
    return ping(host=_arg(command, 1, "192.168.1.10"))


def handle_traceroute(command):
    return traceroute(host=_arg(command, 1, "192.168.1.10"))


def handle_telnet(command):
    return telnet(host=_arg(command, 1, "192.168.1.10"))


def handle_ftp(command):
    return ftp(host=_arg(command, 1, "192.168.1.10"))


def handle_dig(command):
    return dig(domain=_arg(command, 1, "example.com"))


def handle_nslookup(command):
    return nslookup(domain=_arg(command, 1, "example.com"))


def handle_host(command):
    return host(domain=_arg(command, 1, "example.com"))


# ==========================================================
# Main Router Logic
# ==========================================================
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
    elif command.startswith("ping"):
        return handle_ping(command)
    elif command.startswith("ssh"):
        return handle_ssh(command)
    elif command.startswith("telnet"):
        return handle_telnet(command)
    elif command.startswith("ftp"):
        return handle_ftp(command)
    elif command.startswith("traceroute"):
        return handle_traceroute(command)
    elif command.startswith("dig"):
        return handle_dig(command)
    elif command.startswith("nslookup"):
        return handle_nslookup(command)
    elif command == "host" or command.startswith("host "):
        return handle_host(command)

    # --------------------------
    # SYSTEM DISCOVERY
    # --------------------------
    elif command == "hostname":
        return "web-prod-01"
    elif command.startswith("hostnamectl"):
        return handle_hostnamectl(command)
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
    # EXPANSION COMMANDS
    # --------------------------
    elif command.startswith("date"):
        return handle_date(command)
    elif command.startswith("printenv"):
        return handle_printenv(command)
    elif command.startswith("env"):
        return handle_env(command)
    elif command.startswith("echo"):
        return handle_echo(command)
    elif command.startswith("clear"):
        return handle_clear(command)
    elif command.startswith("which"):
        return handle_which(command)
    elif command.startswith("who"):
        return handle_who(command)
    elif command == "w":
        return handle_w(command)
    elif command.startswith("alias"):
        return handle_alias(command)
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