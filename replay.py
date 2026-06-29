import json
import time
from datetime import datetime


def replay_session(file_path):
    with open(file_path, "r") as f:
        session = json.load(f)

    print("=" * 60)
    print("SESSION REPLAY")
    print("=" * 60)
    print(f"Session ID      : {session['session_id']}")
    print(f"Attacker IP     : {session['ip']}")
    print(f"Threat Score    : {session['threat_score']}")
    print(f"Attack Types    : {', '.join(session['attack_types'])}")
    print(f"Session Duration: {session['session_duration']}")
    print("=" * 60)
    print()

    commands = session["commands"]

    for i, cmd in enumerate(commands):

        cwd = cmd.get("cwd", "/home/ubuntu")
        print(f"ubuntu@web-prod-01:{cwd}$ {cmd['command']}")

        if i < len(commands) - 1:
            t1 = datetime.fromisoformat(cmd["timestamp"])
            t2 = datetime.fromisoformat(commands[i + 1]["timestamp"])

            delay = (t2 - t1).total_seconds()

            # Maximum wait 5 seconds
            time.sleep(min(delay, 5))

    print("\nReplay Finished")


if __name__ == "__main__":
   replay_session("logs/session_585ced1a-f200-48ee-aefc-74e863c8387d.json")