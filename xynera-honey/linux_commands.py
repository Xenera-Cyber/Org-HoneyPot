import datetime

def handle_date(command):
    """Returns a realistic Ubuntu date format."""
    now = datetime.datetime.now()
    return now.strftime("%a %b %d %H:%M:%S UTC %Y")

def handle_env(command):
    """Returns a realistic set of root environment variables."""
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

def handle_echo(command):
    """Prints the arguments passed to echo."""
    parts = command.split(" ", 1)
    if len(parts) > 1:
        return parts[1].strip("\"'") 
    return ""

def handle_clear(command):
    """Returns the ANSI escape sequence to physically clear the attacker's screen."""
    return "\033[2J\033[H"

def handle_which(command):
    """Returns standard paths for common Linux binaries."""
    parts = command.split()
    if len(parts) < 2:
        return ""
    
    target = parts[1]
    common_bins = ["ls", "cat", "wget", "curl", "python", "python3", "bash", "sh", "chmod", "chown", "rm", "cp", "mv", "scp", "whoami"]
    
    if target in common_bins:
        return f"/usr/bin/{target}"
    return ""

def handle_who(command):
    """Returns a fake list of logged-in users."""
    return "root     pts/0        2026-06-29 10:14 (192.168.1.45)"

def handle_w(command):
    """Returns a hyper-realistic 'w' command output showing system uptime and users."""
    now = datetime.datetime.now().strftime("%H:%M:%S")
    return f""" {now} up 14 days,  3:12,  1 user,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
root     pts/0    192.168.1.45     10:14    1.00s  0.02s  0.00s -bash"""

def handle_history(command, session_history):
    """Returns the actual commands the attacker has typed in this session."""
    output = ""
    for i, cmd in enumerate(session_history, 1):
        output += f"  {i}  {cmd}\n"
    return output.strip()


# ==========================================
# THE ROUTER
# ==========================================
def route_linux_command(command, session_history):
    """
    Acts just like command_router.py, but strictly for the expansion pack.
    Returns the output if a command is found, otherwise returns None.
    """
    base_command = command.split()[0] if command else ""

    if base_command == "date":
        return handle_date(command)
    elif base_command == "env":
        return handle_env(command)
    elif base_command == "echo":
        return handle_echo(command)
    elif base_command == "clear":
        return handle_clear(command)
    elif base_command == "which":
        return handle_which(command)
    elif base_command == "who":
        return handle_who(command)
    elif base_command == "w":
        return handle_w(command)
    elif base_command == "history":
        return handle_history(command, session_history)
    else:
        return None