import uuid

sessions = {}


def create_session(ip):
    session_id = str(uuid.uuid4())

    sessions[session_id] = {
        "ip": ip,
        "cwd": "/home/ubuntu",
        "commands": []
    }

    return session_id


def get_session(session_id):
    return sessions.get(session_id)

def get_history(session_id):
    return sessions.get(session_id, {}).get("commands", [])

def add_command(session_id, command):
    if session_id in sessions:
        sessions[session_id]["commands"].append(command)
