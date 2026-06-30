import json
import time
from datetime import datetime


def get_replay_speed():
    print("\n========== Select Replay Speed ==========")
    print("1. 0.5x (Slow)")
    print("2. 1x   (Normal)")
    print("3. 1.5x (Fast)")
    print("4. 2x   (Very Fast)")
    print("5. 3x   (Maximum)")

    choice = input("\nEnter your choice (1-5): ")

    speed_map = {
        "1": 0.5,
        "2": 1,
        "3": 1.5,
        "4": 2,
        "5": 3
    }

    return speed_map.get(choice, 1)


def replay_session(file_path):

    speed = get_replay_speed()

    with open(file_path, "r") as f:
        session = json.load(f)

    commands = session["commands"]
    total_commands = len(commands)

    print("\n" + "=" * 60)
    print("                 SESSION REPLAY")
    print("=" * 60)
    print(f"Session ID       : {session['session_id']}")
    print(f"Attacker IP      : {session['ip']}")
    print(f"Attack Types     : {', '.join(session['attack_types'])}")
    print(f"Session Duration : {session['session_duration']}")
    print(f"Replay Speed     : {speed}x")
    print("=" * 60)

    final_score = session["threat_score"]

    score_per_command = (
        final_score / total_commands
        if total_commands > 0
        else 0
    )

    current_score = 0

    for i, cmd in enumerate(commands):

        current_score += score_per_command

        print("\n" + "-" * 50)
        print(f"Command Counter : {i+1}/{total_commands}")
        print(f"Timestamp       : {cmd['timestamp']}")
        print(f"Threat Score    : {int(current_score)}")
        print("-" * 50)

        cwd = cmd.get("cwd", "/home/ubuntu")

        print(f"ubuntu@web-prod-01:{cwd}$ {cmd['command']}")

        # Pause / Resume
        while True:

            option = input(
                "\n[ENTER] Continue | [P] Pause | [Q] Quit : "
            ).strip().lower()

            if option == "":
                break

            elif option == "p":

                print("\n========== REPLAY PAUSED ==========")

                while True:

                    resume = input(
                        "Press R to Resume : "
                    ).strip().lower()

                    if resume == "r":
                        print("\nReplay Resumed...")
                        break
                    else:
                        print("Invalid Input!")

                break

            elif option == "q":

                print("\nReplay Cancelled.")
                return

            else:

                print("Invalid Choice!")

        if i < total_commands - 1:

            t1 = datetime.fromisoformat(
                cmd["timestamp"]
            )

            t2 = datetime.fromisoformat(
                commands[i + 1]["timestamp"]
            )

            delay = (
                t2 - t1
            ).total_seconds()

            delay = delay / speed

            time.sleep(min(delay, 5))

    print("\n" + "=" * 60)
    print("                 REPLAY SUMMARY")
    print("=" * 60)

    print("Replay Status      : Completed Successfully")
    print(f"Replay Speed       : {speed}x")
    print(f"Session ID         : {session['session_id']}")
    print(f"Attacker IP        : {session['ip']}")
    print(f"Total Commands     : {total_commands}")
    print(f"Commands Replayed  : {total_commands}")
    print(f"Attack Types       : {', '.join(session['attack_types'])}")
    print(f"Final Threat Score : {session['threat_score']}")
    print(f"Session Duration   : {session['session_duration']}")

    print("=" * 60)
    print("Replay Completed Successfully")
    print("=" * 60)


if __name__ == "__main__":
    replay_session(
        "logs/session_585ced1a-f200-48ee-aefc-74e863c8387d.json"
    )