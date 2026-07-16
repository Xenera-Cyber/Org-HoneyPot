import time
import random
import shlex
from datetime import datetime

import ai_client  # Added AI client utility mapping
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

HOME_DIR = "/home/ubuntu"

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
    return "root      pts/0        2026-06-29 10:14 (192.168.1.45)"


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
    """
    Render shell-style history from session["command_history"].
    Supports `history -c` to clear it and `history N` to show only the
    last N entries (original line numbers are preserved, matching real
    bash behaviour).
    """
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


def handle_chmod(command):
    """
    Bug fix: chmod previously reported "Permissions updated" for any
    input at all, including missing or nonsensical modes. It now
    validates the mode argument like a real chmod would.
    """
    parts = command.split()
    if len(parts) < 3:
        return "chmod: missing operand"

    permission = parts[1]
    valid_permissions = ["+x", "-x", "777", "755", "644", "600"]
    if permission not in valid_permissions:
        return f"chmod: invalid mode: '{permission}'"

    return "Permissions updated"


def handle_service(command, services):
    """`service <name> {start|stop|restart}` — backed by session_manager.services."""
    parts = command.split()
    if len(parts) < 3:
        return "Usage: service <name> {start|stop|restart}"
    name, action = parts[1], parts[2]
    return services.handle_service_command(name, action)


def handle_systemctl(command, services):
    """
    `systemctl status <name>` / `systemctl {start|stop|restart} <name>`,
    backed by session_manager.services so state agrees with `service`,
    netstat, and ss for the rest of the session.
    """
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
# Network Command Helpers (shared arg-parsing, avoids duplication)
# ==========================================================
def _arg(command, index=1, default=None):
    parts = command.split()
    return parts[index] if len(parts) > index else default


def handle_ssh(command):
    """Supports `ssh [-p port] [user@]host`."""
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
    """Supports `ping [-c count] host`."""
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
# Filesystem Command Helpers (dynamic, session-scoped filesystem)
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

    time.sleep(get_command_delay(command))

    # --------------------------
    # DECEPTION ENGINE
    # --------------------------
    deception_response = deception_engine.adapt_response(command, session, attack_type)
    if deception_response is not None:
        return deception_response

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
        return "14:23:05 up 37 days, 3 users, load average: 0.11, 0.09, 0.05"
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
        return handle_chmod(command)
    elif command.startswith("nc"):
        return "Connection established"

    # --------------------------
    # DEFAULT -> AI FALLBACK
    # --------------------------
    ai_result = ai_client.send_to_ai(
        ip=session["attacker_ip"],
        command=command,
        history=session["command_history"],
        attack_type=attack_type,
        session_id=session["session_id"],
        cwd=cwd,
    )
    if ai_result and ai_result.get("backend") == "local":
        # Personality is analyst metadata only — it is NEVER used to
        # change the attacker-visible hostname/username. See
        # session_manager.py for why.
        session_manager.update_personality(
            personality_name=ai_result.get("personality_name"),
        )
        if ai_result.get("reply"):
            return ai_result["reply"]

    # AI backend offline/timed out/empty reply — degrade gracefully
    return f"{command}: command not found"