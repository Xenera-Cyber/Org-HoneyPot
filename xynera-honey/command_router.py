import time
import random
import shlex
from datetime import datetime

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
import ai_client

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
# Backend Synchronization Helpers
# ==========================================================
def _cache_key(command_type, *parts):
    return ":".join([command_type, *(str(part) for part in parts)])


def _prefixed_response(command, handlers, *args):
    for prefix, handler in handlers:
        if command.startswith(prefix):
            return handler(command, *args)
    return None


def _backend_read(session_manager, key, local_reader):
    if session_manager.backend_exists(key):
        return session_manager.get_backend(key)

    response = local_reader()
    session_manager.save_backend(key, response)
    return response


def _backend_write(session_manager, local_writer):
    response = local_writer()
    session_manager.sync_backend_after_filesystem_write()
    return response


def _synced_service_response(session_manager, handler, command, services):
    response = handler(command, services)
    session_manager.sync_service_state()
    return response


def _group_id(group):
    known_groups = {
        "root": 0,
        "sudo": 27,
        "docker": 999,
        "lxd": 110,
    }
    return known_groups.get(group, 1000)


def _identity_ids(session_manager):
    if session_manager.username == "root":
        return 0, 0
    return 1000, 1000


def _expand_home(path, session_manager):
    if session_manager is None:
        return path
    if path == "~":
        return session_manager.home_dir
    if path.startswith("~/"):
        return f"{session_manager.home_dir}/{path[2:]}"
    return path


def _current_environment(session_manager):
    environment = dict(session_manager.environment)
    environment["PWD"] = session_manager.get_cwd()
    return environment


# ==========================================================
# Expansion Pack Helper Functions
# ==========================================================
def handle_date(command):
    return datetime.now().strftime("%a %b %d %H:%M:%S UTC %Y")


<<<<<<< HEAD
def handle_env(command, identity):
    """
    Bug fix: previously hardcoded USER=root / HOME=/root / LOGNAME=root,
    which contradicted whoami/id reporting the session's actual username.
    Now built from the same session identity as every other command.
    """
    username = identity["username"]
    home = "/root" if username == "root" else f"/home/{username}"
    return f"""SHELL=/bin/bash
PWD={home}
LOGNAME={username}
HOME={home}
LANG=en_US.UTF-8
LS_COLORS=rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:
LESSCLOSE=/usr/bin/lesspipe %s %s
TERM=xterm-256color
LESSOPEN=| /usr/bin/lesspipe %s
USER={username}
SHLVL=1
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
_=/usr/bin/env"""


def handle_printenv(command, identity):
    return handle_env(command, identity)
=======
def handle_env(command, session_manager):
    environment = _current_environment(session_manager)
    return "\n".join(f"{key}={value}" for key, value in environment.items())


def handle_printenv(command, session_manager):
    parts = command.split()
    if len(parts) > 1:
        return _current_environment(session_manager).get(parts[1], "")
    return handle_env(command, session_manager)
>>>>>>> origin/hriday/baseline-v3.3


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


<<<<<<< HEAD
def handle_who(command, identity):
    now = "2026-06-29 10:14"
    return f"{identity['username']:<9}pts/0        {now} (192.168.1.45)"


def handle_w(command, identity):
    now = datetime.now().strftime("%H:%M:%S")
    return f""" {now} up 14 days,  3:12,  1 user,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
{identity['username']:<9}pts/0    192.168.1.45     10:14    1.00s  0.02s  0.00s -bash"""
=======
def handle_who(command, session_manager):
    """
    Bug fix: previously hardcoded "root" regardless of the session's
    actual identity. Now reads it from the same source of truth as
    whoami/id/env (session_manager).
    """
    return f"{session_manager.username:<9}pts/0        2026-06-29 10:14 (192.168.1.45)"


def handle_w(command, session_manager):
    """Bug fix: same stale-"root" issue as handle_who(); see above."""
    now = datetime.now().strftime("%H:%M:%S")
    return f""" {now} up 14 days,  3:12,  1 user,  load average: 0.00, 0.00, 0.00
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
{session_manager.username:<9}pts/0    192.168.1.45     10:14    1.00s  0.02s  0.00s -bash"""
>>>>>>> origin/hriday/baseline-v3.3


def handle_alias(command):
    return """alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'
alias grep='grep --color=auto'
alias l='ls -CF'
alias la='ls -A'
alias ll='ls -alF'
alias ls='ls --color=auto'"""


<<<<<<< HEAD
def handle_hostnamectl(command, identity):
    """
    Bug fix: this previously hardcoded "xynera-server" as the static
    hostname, while the plain `hostname` command reported "web-prod-01"
    -- two different hostnames for the same machine in the same session.
    Both now read from the same session identity.
    """
    return f"""   Static hostname: {identity['hostname']}
=======
def handle_hostnamectl(command, session_manager):
    return f"""   Static hostname: {session_manager.hostname}
>>>>>>> origin/hriday/baseline-v3.3
         Icon name: computer-vm
           Chassis: vm
        Machine ID: 8a4e8d3a5b6c4f729e1f2d3c4b5a6978
           Boot ID: 1b2c3d4f5a6b7c8d9e0f1a2b3c4d5e6f
    Virtualization: kvm
  Operating System: Ubuntu 22.04.3 LTS
            Kernel: Linux {session_manager.kernel_version}
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


SESSION_EXPANSION_HANDLERS = (
    ("printenv", handle_printenv), ("env", handle_env),
    ("history", handle_history), ("who", handle_who),
)

EXPANSION_HANDLERS = (
    ("date", handle_date), ("echo", handle_echo),
    ("clear", handle_clear), ("which", handle_which),
    ("alias", handle_alias),
)


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


NETWORK_PREFIX_HANDLERS = (
    ("ping", handle_ping), ("ssh", handle_ssh),
    ("telnet", handle_telnet), ("ftp", handle_ftp),
    ("traceroute", handle_traceroute), ("dig", handle_dig),
    ("nslookup", handle_nslookup),
)

NETWORK_EXACT_HANDLERS = {
    "netstat": netstat, "netstat -tulpn": netstat_tulpn, "ss": ss,
}

NETWORK_STATIC_HANDLERS = {
    "ifconfig": ifconfig, "ip addr": ip_addr,
}


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


def _split_flags_paths(parts):
    return (
        [part for part in parts[1:] if part.startswith("-")],
        [part for part in parts[1:] if not part.startswith("-")],
    )


def _handle_create(command, filesystem, cwd, creator, session_manager=None):
    parts, error = _split_command(command)
    if error:
        return error
    if len(parts) < 2:
        return creator(cwd, "")
    return _collect_errors(
        creator(cwd, _expand_home(path, session_manager))
        for path in parts[1:]
        if not path.startswith("-")
    )


def handle_ls(command, filesystem, cwd, session_manager=None):
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
    if target and session_manager is not None:
        target = _expand_home(target, session_manager)
    target_path = filesystem.resolve_path(cwd, target) if target else cwd

    def local_read():
        return filesystem.ls(
            cwd,
            path=target,
            show_all=show_all,
            long_format=long_format,
        )

    if session_manager is None:
        return local_read()

    key = _cache_key("fs", "ls", target_path, show_all, long_format)
    return _backend_read(session_manager, key, local_read)


def handle_touch(command, filesystem, cwd, session_manager=None):
    return _handle_create(command, filesystem, cwd, filesystem.touch, session_manager)


def handle_mkdir(command, filesystem, cwd, session_manager=None):
    return _handle_create(command, filesystem, cwd, filesystem.mkdir, session_manager)


def handle_rm(command, filesystem, cwd, session_manager=None):
    parts, error = _split_command(command)
    if error:
        return error
    if len(parts) < 2:
        return filesystem.rm(cwd, "")

    flags, paths = _split_flags_paths(parts)
    recursive = any("r" in flag or "R" in flag for flag in flags)
    force = any("f" in flag for flag in flags)
    if not paths:
        return "" if force else filesystem.rm(cwd, "")
    return _collect_errors(
        filesystem.rm(
            cwd,
            _expand_home(path, session_manager),
            recursive=recursive,
            force=force,
        )
        for path in paths
    )


def handle_mv(command, filesystem, cwd, session_manager=None):
    parts, error = _split_command(command)
    if error:
        return error
    if len(parts) < 3:
        return "mv: missing file operand"
    return filesystem.mv(
        cwd,
        _expand_home(parts[1], session_manager),
        _expand_home(parts[2], session_manager),
    )


def handle_cp(command, filesystem, cwd, session_manager=None):
    parts, error = _split_command(command)
    if error:
        return error
    if len(parts) < 3:
        return "cp: missing file operand"

    flags, operands = _split_flags_paths(parts)
    if len(operands) < 2:
        return "cp: missing destination file operand"
    recursive = any("r" in flag or "R" in flag for flag in flags)
    return filesystem.cp(
        cwd,
        _expand_home(operands[0], session_manager),
        _expand_home(operands[1], session_manager),
        recursive=recursive,
    )


FILESYSTEM_WRITE_HANDLERS = {
    "touch": handle_touch, "mkdir": handle_mkdir, "rm": handle_rm,
    "mv": handle_mv, "cp": handle_cp,
}

# Commands that create brand-new nodes — ownership must be fixed up after write.
_CREATES_NEW_NODE = {"touch", "mkdir", "cp"}


def _chown_new_nodes(command, verb, filesystem, cwd, session_manager):
    """Apply the session's current ownership to any node just created.

    Only called for verbs that create new filesystem nodes (touch/mkdir/cp).
    Resolves the destination path from the command and delegates to
    session_manager._apply_ownership(), which already recurses into
    directories, so cp -r is covered for free.
    """
    owner = session_manager.username
    group = session_manager.groups[0]
    parts, error = _split_command(command)
    if error or len(parts) < 2:
        return
    # Destination is always the last non-flag argument.
    dest = next(
        (p for p in reversed(parts[1:]) if not p.startswith("-")),
        None,
    )
    if dest is None:
        return
    dest_path = filesystem.resolve_path(cwd, _expand_home(dest, session_manager))
    session_manager._apply_ownership(dest_path, owner, group)


def _filesystem_write_response(command, session_manager, filesystem, cwd):
    verb = command.partition(" ")[0]
    handler = FILESYSTEM_WRITE_HANDLERS[verb]
    result = _backend_write(
        session_manager,
        lambda: handler(command, filesystem, cwd, session_manager),
    )
    if verb in _CREATES_NEW_NODE:
        _chown_new_nodes(command, verb, filesystem, cwd, session_manager)
    return result


def handle_cat(command, filesystem, cwd, session_manager):
    path = _expand_home(command[4:].strip(), session_manager)
    target_path = filesystem.resolve_path(cwd, path)
    key = _cache_key("fs", "cat", target_path)
    return _backend_read(
        session_manager,
        key,
        lambda: filesystem.cat(cwd, path),
    )


def handle_pwd(filesystem, cwd, session_manager):
    key = _cache_key("fs", "pwd", cwd)
    return _backend_read(
        session_manager,
        key,
        lambda: filesystem.pwd(cwd),
    )


def handle_cd(command, filesystem, cwd, session_manager):
    path = command[2:].strip()
    path = session_manager.home_dir if not path else _expand_home(path, session_manager)
    target_path = filesystem.resolve_path(cwd, path)
    key = _cache_key("fs", "cd", target_path)
    new_path, error = _backend_read(
        session_manager,
        key,
        lambda: filesystem.cd(cwd, path),
    )
    if not error:
        session_manager.change_directory(new_path)
        return ""
    return error


ATTACKER_PREFIX_HANDLERS = (
    ("wget", lambda command: malware_detector.handle_wget(command)[0]),
    ("curl", lambda command: malware_detector.handle_curl(command)[0]),
    ("scp", lambda command: malware_detector.handle_scp(command)[0]),
    ("chmod", handle_chmod),
    ("nc", lambda command: "Connection established"),
)


def _attacker_response(command):
    return _prefixed_response(command, ATTACKER_PREFIX_HANDLERS)


# ==========================================================
# Main Router Logic
# ==========================================================
def route_command(command, session_manager, attack_type="Unknown"):
    session = session_manager.get_session()
    cwd = session_manager.get_cwd()
    filesystem = session_manager.filesystem
    services = session_manager.service_manager
    command = command.strip()

    # Single source of truth for identity. Every command below that
    # needs a username/hostname reads it from here -- never hardcoded.
    identity = session_manager.get_identity()

    time.sleep(get_command_delay(command))

    # --------------------------
    # DECEPTION ENGINE
    # --------------------------
    # Gives select attack types (credential probing for files that don't
    # exist in the simulated filesystem, dynamic uptime, etc.) a chance
    # to override the standard response below. Returns None for most
    # commands, in which case normal routing proceeds unchanged.
    deception_response = deception_engine.adapt_response(command, session, attack_type)
    if deception_response is not None:
        return deception_response

    if command == "whoami":
<<<<<<< HEAD
        return identity["username"]
    elif command == "groups":
        return f"{identity['username']} sudo docker"
    elif command == "id":
        username = identity["username"]
        return (
            f"uid=1000({username}) "
            f"gid=1000({username}) "
            f"groups=1000({username})"
        )
    elif command == "users":
        return identity["username"]
=======
        return session_manager.username
    elif command == "groups":
        return " ".join(session_manager.groups)
    elif command == "id":
        uid, gid = _identity_ids(session_manager)
        group_entries = [
            f"{_group_id(group)}({group})"
            for group in session_manager.groups
        ]
        return (
            f"uid={uid}({session_manager.username}) "
            f"gid={gid}({session_manager.groups[0]}) "
            f"groups={','.join(group_entries)}"
        )
    elif command == "users":
        return session_manager.username
>>>>>>> origin/hriday/baseline-v3.3

    elif command == "pwd":
        return handle_pwd(filesystem, cwd, session_manager)
    elif command == "ls" or command.startswith("ls "):
        return handle_ls(command, filesystem, cwd, session_manager)

    elif command == "cd" or command.startswith("cd "):
        return handle_cd(command, filesystem, cwd, session_manager)

    elif command.startswith("cat "):
        return handle_cat(command, filesystem, cwd, session_manager)
    elif command.partition(" ")[0] in FILESYSTEM_WRITE_HANDLERS:
        return _filesystem_write_response(command, session_manager, filesystem, cwd)

    elif command == "ps":
        return ps()
    elif command == "ps aux":
<<<<<<< HEAD
        return ps_aux(username=identity["username"])
=======
        # ps_aux() takes the live session username so the attacker's own
        # shell/`ps aux` rows never show a stale identity (see
        # fake_process.py).
        return ps_aux(username=session_manager.username)
>>>>>>> origin/hriday/baseline-v3.3

    elif command in NETWORK_EXACT_HANDLERS:
        return NETWORK_EXACT_HANDLERS[command](services)
    elif command in NETWORK_STATIC_HANDLERS:
        return NETWORK_STATIC_HANDLERS[command]()
    elif any(command.startswith(prefix) for prefix, _handler in NETWORK_PREFIX_HANDLERS):
        return _prefixed_response(command, NETWORK_PREFIX_HANDLERS)
    elif command == "host" or command.startswith("host "):
        return handle_host(command)

    elif command == "hostname":
<<<<<<< HEAD
        return identity["hostname"]
    elif command.startswith("hostnamectl"):
        return handle_hostnamectl(command, identity)
    elif command == "uname -a":
        return f"Linux {identity['hostname']} 5.15.0-generic x86_64 GNU/Linux"
=======
        return session_manager.hostname
    elif command.startswith("hostnamectl"):
        return handle_hostnamectl(command, session_manager)
    elif command == "uname -a":
        return (
            f"Linux {session_manager.hostname} "
            f"{session_manager.kernel_version} x86_64 GNU/Linux"
        )
>>>>>>> origin/hriday/baseline-v3.3
    elif command == "uptime":
        return "14:23:05 up 37 days, 3 users, load average: 0.11, 0.09, 0.05"
    elif command == "systemctl" or command.startswith("systemctl "):
        return _synced_service_response(session_manager, handle_systemctl, command, services)
    elif command.startswith("service "):
        return _synced_service_response(session_manager, handle_service, command, services)

<<<<<<< HEAD
    # --------------------------
    # EXPANSION COMMANDS
    # --------------------------
    elif command.startswith("date"):
        return handle_date(command)
    elif command.startswith("printenv"):
        return handle_printenv(command, identity)
    elif command.startswith("env"):
        return handle_env(command, identity)
    elif command.startswith("echo"):
        return handle_echo(command)
    elif command.startswith("clear"):
        return handle_clear(command)
    elif command.startswith("which"):
        return handle_which(command)
    elif command.startswith("who"):
        return handle_who(command, identity)
    elif command == "w":
        return handle_w(command, identity)
    elif command.startswith("alias"):
        return handle_alias(command)
    elif command.startswith("history"):
        return handle_history(command, session_manager)
=======
    elif any(command.startswith(prefix) for prefix, _handler in SESSION_EXPANSION_HANDLERS):
        return _prefixed_response(command, SESSION_EXPANSION_HANDLERS, session_manager)
    elif any(command.startswith(prefix) for prefix, _handler in EXPANSION_HANDLERS):
        return _prefixed_response(command, EXPANSION_HANDLERS)
    elif command == "w":
        return handle_w(command, session_manager)

    elif any(command.startswith(prefix) for prefix, _handler in ATTACKER_PREFIX_HANDLERS):
        return _attacker_response(command)
>>>>>>> origin/hriday/baseline-v3.3

    # --------------------------
    # DEFAULT -> AI FALLBACK
    # --------------------------
    # Nothing in the static routing table above matched. Before giving up
    # with "command not found", give the AI backend a chance to improvise
    # a plausible response for this session.
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

    # AI backend offline/timed out/empty reply — degrade gracefully.
    return f"{command}: command not found"

