import time
import random
import shlex
from datetime import datetime, timedelta

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
from fake_process import ps, ps_aux
import malware_detector
import deception_engine
import fake_advanced  # Imported for Task 2

HOME_DIR = "/home/ubuntu"

# ==========================================================
# Task 3: Dynamic System Boot Time
# Generated once when the module loads so it remains consistent
# ==========================================================
SYSTEM_BOOT_TIME = datetime.now() - timedelta(
    days=random.randint(14, 45), 
    hours=random.randint(1, 23), 
    minutes=random.randint(1, 59)
)

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
    "touch": 0.2,
    "mkdir": 0.2,
    "rm": 0.3,
    "mv": 0.3,
    "cp": 0.3,
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
    "service": 0.3,
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
def get_uptime_string():
    """Helper to generate consistent, ticking Linux uptime string."""
    now = datetime.now()
    delta = now - SYSTEM_BOOT_TIME
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    
    current_time = now.strftime("%H:%M:%S")
    
    if days > 0:
        return f"{current_time} up {days} days, {hours:>2}:{minutes:02d}"
    else:
        return f"{current_time} up {hours:>2}:{minutes:02d}"


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
        "chmod", "chown", "rm", "cp", "mv", "scp", "whoami", "nc", "netcat"
    ]
    if target in common_bins:
        return f"/usr/bin/{target}"
    return ""


def handle_who(command, session_manager):
    session = session_manager.get_session()
    ip = session.get("attacker_ip", "192.168.1.45")
    
    try:
        start_dt = datetime.fromisoformat(session.get("start_time", datetime.now().isoformat()))
        login_time = start_dt.strftime("%Y-%m-%d %H:%M")
    except:
        login_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        
    username = "ubuntu"
    if hasattr(session_manager, 'get_username'):
        username = session_manager.get_username()
        
    return f"{username:<8} pts/0        {login_time} ({ip})"


def handle_w(command, session_manager):
    session = session_manager.get_session()
    ip = session.get("attacker_ip", "192.168.1.45")
    
    try:
        start_dt = datetime.fromisoformat(session.get("start_time", datetime.now().isoformat()))
        login_time = start_dt.strftime("%H:%M")
    except:
        login_time = datetime.now().strftime("%H:%M")
        
    username = "ubuntu"
    if hasattr(session_manager, 'get_username'):
        username = session_manager.get_username()
        
    up_str = get_uptime_string()
    load1 = round(random.uniform(0.0, 0.1), 2)
    load5 = round(random.uniform(0.0, 0.1), 2)
    load15 = round(random.uniform(0.0, 0.05), 2)
    
    return f""" {up_str},  1 user,  load average: {load1:.2f}, {load5:.2f}, {load15:.2f}
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
{username:<8} pts/0    {ip:<16} {login_time:<8} 1.00s  0.02s  0.00s -bash"""


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
    history = session.get("command_history", [])
    parts = command.split()

    if "-c" in parts:
        history.clear()
        return ""

    numbered = list(enumerate(history, 1))
    if len(parts) > 1 and parts[1].isdigit():
        limit = int(parts[1])
        numbered = numbered[-limit:]

    if not numbered:
        return ""
    return "\n".join(f"  {i}  {entry['command']}" for i, entry in numbered)


def handle_service(command, services):
    parts = command.split()
    if len(parts) < 3:
        return "Usage: service <name> {start|stop|restart}"
    name, action = parts[1], parts[2]
    return services.handle_service_command(name, action)


def handle_systemctl(command, services):
    parts = command.split()
    if len(parts) < 2:
        return services.systemctl_overview()

    sub = parts[1]
    if sub == "status" and len(parts) >= 3:
        return services.systemctl_status(parts[2])
    if sub in ("start", "stop", "restart") and len(parts) >= 3:
        return services.handle_service_command(parts[2], sub)
    return services.systemctl_overview()


# ==========================================================
# Network Command Helpers
# ==========================================================
def _arg(command, index=1, default=None):
    parts = command.split()
    return parts[index] if len(parts) > index else default


def handle_ssh(command):
    parts = command.split()[1:]
    port = 22
    user = "root"
    target = "192.168.1.10"

    positional = []
    i = 0
    while i < len(parts):
        if parts[i] == "-p" and i + 1 < len(parts):
            if parts[i + 1].isdigit():
                port = int(parts[i + 1])
            i += 2
            continue
        if not parts[i].startswith("-"):
            positional.append(parts[i])
        i += 1

    if positional:
        last = positional[-1]
        if "@" in last:
            user, target = last.split("@", 1)
        else:
            target = last

    return ssh(host=target, user=user, port=port)


def handle_ping(command):
    parts = command.split()[1:]
    count = 3
    target = "192.168.1.10"

    i = 0
    while i < len(parts):
        if parts[i] == "-c" and i + 1 < len(parts):
            if parts[i + 1].isdigit():
                count = int(parts[i + 1])
            i += 2
            continue
        if not parts[i].startswith("-"):
            target = parts[i]
        i += 1

    return ping(host=target, count=count)


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
# Filesystem Command Helpers
# ==========================================================
def _split_command(command):
    try:
        return shlex.split(command), None
    except ValueError as exc:
        return None, f"bash: {exc}"


def _collect_errors(results):
    return "\n".join(result for result in results if result)


def handle_ls(command, filesystem, cwd):
    parts, error = _split_command(command)
    if error:
        return error

    flags = []
    paths = []
    for part in parts[1:]:
        if part.startswith("-"):
            flags.append(part)
        else:
            paths.append(part)

    long_format = any("l" in flag for flag in flags)
    show_all = True if not flags else any("a" in flag for flag in flags)
    target = paths[0] if paths else ""
    return filesystem.ls(
        cwd,
        path=target,
        show_all=show_all,
        long_format=long_format,
    )


def handle_touch(command, filesystem, cwd):
    parts, error = _split_command(command)
    if error:
        return error
    if len(parts) < 2:
        return filesystem.touch(cwd, "")
    return _collect_errors(
        filesystem.touch(cwd, path)
        for path in parts[1:]
        if not path.startswith("-")
    )


def handle_mkdir(command, filesystem, cwd):
    parts, error = _split_command(command)
    if error:
        return error
    if len(parts) < 2:
        return filesystem.mkdir(cwd, "")
    return _collect_errors(
        filesystem.mkdir(cwd, path)
        for path in parts[1:]
        if not path.startswith("-")
    )


def handle_rm(command, filesystem, cwd):
    parts, error = _split_command(command)
    if error:
        return error
    if len(parts) < 2:
        return filesystem.rm(cwd, "")

    flags = [part for part in parts[1:] if part.startswith("-")]
    paths = [part for part in parts[1:] if not part.startswith("-")]
    recursive = any("r" in flag or "R" in flag for flag in flags)
    force = any("f" in flag for flag in flags)
    if not paths:
        return "" if force else filesystem.rm(cwd, "")
    return _collect_errors(
        filesystem.rm(cwd, path, recursive=recursive, force=force)
        for path in paths
    )


def handle_mv(command, filesystem, cwd):
    parts, error = _split_command(command)
    if error:
        return error
    if len(parts) < 3:
        return "mv: missing file operand"
    return filesystem.mv(cwd, parts[1], parts[2])


def handle_cp(command, filesystem, cwd):
    parts, error = _split_command(command)
    if error:
        return error
    if len(parts) < 3:
        return "cp: missing file operand"

    flags = [part for part in parts[1:] if part.startswith("-")]
    operands = [part for part in parts[1:] if not part.startswith("-")]
    if len(operands) < 2:
        return "cp: missing destination file operand"
    recursive = any("r" in flag or "R" in flag for flag in flags)
    return filesystem.cp(cwd, operands[0], operands[1], recursive=recursive)


# ==========================================================
# Main Router Logic
# ==========================================================
def route_command(command, session_manager, attack_type="Unknown"):
    session = session_manager.get_session()
    cwd = session["cwd"]
    filesystem = session_manager.filesystem
    services = session_manager.services
    command = command.strip()
    cmd_parts = command.split()
    base_cmd = cmd_parts[0] if cmd_parts else ""

    time.sleep(get_command_delay(command))

    # --------------------------
    # DECEPTION ENGINE
    # --------------------------
    deception_response = deception_engine.adapt_response(command, session, attack_type)
    if deception_response is not None:
        return deception_response

    # --------------------------
    # COMMON BLOCKED COMMANDS (Task 2)
    # --------------------------
    blocked_commands = ["apt-get", "apt", "yum", "dpkg", "npm", "pip", "git", "vim", "nano"]
    if base_cmd in blocked_commands:
         return fake_advanced.get_common_error(base_cmd, "", "permission_denied")

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
        return filesystem.pwd(cwd)
    elif command == "ls" or command.startswith("ls "):
        return handle_ls(command, filesystem, cwd)

    # --------------------------
    # CHANGE DIRECTORY
    # --------------------------
    elif command == "cd" or command.startswith("cd "):
        path = command[2:].strip()
        new_path, error = filesystem.cd(cwd, path)
        if not error:
            session_manager.change_directory(new_path)
            return ""
        return error

    # --------------------------
    # FILE COMMANDS
    # --------------------------
    elif command.startswith("cat "):
        filename = command[4:].strip()
        return filesystem.cat(cwd, filename)
    elif command == "touch" or command.startswith("touch "):
        return handle_touch(command, filesystem, cwd)
    elif command == "mkdir" or command.startswith("mkdir "):
        return handle_mkdir(command, filesystem, cwd)
    elif command == "rm" or command.startswith("rm "):
        return handle_rm(command, filesystem, cwd)
    elif command == "mv" or command.startswith("mv "):
        return handle_mv(command, filesystem, cwd)
    elif command == "cp" or command.startswith("cp "):
        return handle_cp(command, filesystem, cwd)

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
        return netstat(services)
    elif command == "netstat -tulpn":
        return netstat_tulpn(services)
    elif command == "ss":
        return ss(services)
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
        up_str = get_uptime_string()
        load1 = round(random.uniform(0.0, 0.1), 2)
        load5 = round(random.uniform(0.0, 0.1), 2)
        load15 = round(random.uniform(0.0, 0.05), 2)
        return f" {up_str},  1 user,  load average: {load1:.2f}, {load5:.2f}, {load15:.2f}"
    elif command == "systemctl" or command.startswith("systemctl "):
        return handle_systemctl(command, services)
    elif command.startswith("service "):
        return handle_service(command, services)

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
        return handle_who(command, session_manager)
    elif command == "w":
        return handle_w(command, session_manager)
    elif command.startswith("alias"):
        return handle_alias(command)
    elif command.startswith("history"):
        return handle_history(command, session_manager)

    # --------------------------
    # ATTACKER COMMANDS (Task 2 Integrated)
    # --------------------------
    elif command.startswith("wget"):
        return malware_detector.handle_wget(command)[0]
    elif command.startswith("curl"):
        return malware_detector.handle_curl(command)[0]
    elif command.startswith("scp"):
        return malware_detector.handle_scp(command)[0]
    elif command.startswith("chmod"):
        args = " ".join(cmd_parts[1:])
        return fake_advanced.chmod(args)
    elif command.startswith("nc") or command.startswith("netcat"):
        args = " ".join(cmd_parts[1:])
        return fake_advanced.nc(args)

    # --------------------------
    # DEFAULT (Task 2 Error Handlers)
    # --------------------------
    return fake_advanced.get_common_error(base_cmd, "", "not_found")