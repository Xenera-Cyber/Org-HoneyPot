from ai_client import send_to_ai
from fake_filesystem import ls, cd, pwd, cat
from fake_process import ps
from fake_network import netstat, ss
from attack_analyzer import classify
from deception_engine import adapt_response


def route_command(command, session):
    ip = session["ip"]

    parts = command.split()
    cmd = parts[0] if parts else ""

    # define attack type once
    attack_type = classify(command)

    # ===== LOCAL COMMANDS =====
    if cmd == "ls":
        return ls(session), attack_type

    elif cmd == "pwd":
        return pwd(session), attack_type

    elif cmd == "cd":
        if len(parts) < 2:
            return "", attack_type
        return cd(session, parts[1]), attack_type

    elif cmd == "cat":
        if len(parts) < 2:
            return "cat: missing file", attack_type
        return cat(session, parts[1]), attack_type

    elif cmd == "ps":
        return ps(), attack_type

    elif cmd == "netstat":
        return netstat(), attack_type

    elif cmd == "ss":
        return ss(), attack_type

    elif cmd == "whoami":
        return "ubuntu", attack_type

    elif cmd == "id":
        return "uid=1000(ubuntu) gid=1000(ubuntu) groups=1000(ubuntu)", attack_type

    # ===== ADAPTIVE DECEPTION =====
    deception = adapt_response(command, session, attack_type)

    if deception is not None:
        return deception, attack_type

    # ===== AI WITH CONTEXT =====
    history = session.get("commands", [])[-5:]

    return send_to_ai(ip, command, history, attack_type), attack_type
