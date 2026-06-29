import re
from collections import Counter

from attack_analyzer import threat_score

LOG_FILE = "logs/attacks.log"


# ==========================================================
# Log Parser
# ==========================================================

LOG_PATTERN = re.compile(
    r"\[(.*?)\]\s"
    r"\[(.*?)\]\s"
    r"IP=(.*?)\s\|\s"
    r"SESSION=(.*?)\s\|\s"
    r"TYPE=(.*?)\s\|\s"
    r"CMD=(.*)"
)


def load_logs():
    """
    Load and parse all log entries.
    """

    logs = []

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as file:

            for line in file:

                match = LOG_PATTERN.match(line.strip())

                if not match:
                    continue

                logs.append({

                    "timestamp": match.group(1),

                    "severity": match.group(2),

                    "ip": match.group(3),

                    "session": match.group(4),

                    "attack_type": match.group(5),

                    "command": match.group(6)
                })

    except FileNotFoundError:

        print("\nLog file not found.\n")

    return logs


# ==========================================================
# Display Utility
# ==========================================================

def print_logs(logs):

    if not logs:
        print("\nNo matching logs found.\n")
        return

    for log in logs:

        print("-" * 70)

        print(f"Timestamp : {log['timestamp']}")
        print(f"Severity  : {log['severity']}")
        print(f"IP        : {log['ip']}")
        print(f"Session   : {log['session']}")
        print(f"Attack    : {log['attack_type']}")
        print(f"Command   : {log['command']}")

    print("-" * 70)


# ==========================================================
# Latest Logs
# ==========================================================

def latest_logs(logs):

    try:

        n = int(input("\nNumber of latest logs: "))

    except ValueError:

        print("Invalid input.")
        return

    print_logs(logs[-n:])


# ==========================================================
# Filter by IP
# ==========================================================

def filter_ip(logs):

    ip = input("\nEnter IP Address: ").strip()

    result = [

        log

        for log in logs

        if log["ip"] == ip
    ]

    print_logs(result)


# ==========================================================
# Filter by Attack Type
# ==========================================================

def filter_attack(logs):

    attack = input("\nEnter Attack Type: ").strip()

    result = [

        log

        for log in logs

        if log["attack_type"].lower() == attack.lower()
    ]

    print_logs(result)


# ==========================================================
# Filter by Severity
# ==========================================================

def filter_severity(logs):

    severity = input("\nEnter Severity: ").strip()

    result = [

        log

        for log in logs

        if log["severity"].lower() == severity.lower()
    ]

    print_logs(result)


# ==========================================================
# Threat Summary
# ==========================================================

def threat_summary(logs):

    attack_counter = Counter()

    total_score = 0

    for log in logs:

        attack = log["attack_type"]

        attack_counter[attack] += 1

        total_score += threat_score(attack)

    print("\n========== Threat Summary ==========\n")

    for attack, count in attack_counter.items():

        score = threat_score(attack)

        print(

            f"{attack:<28}"

            f"Count: {count:<3}"

            f"Score: {score * count}"
        )

    print("\n-----------------------------------")

    print(f"Total Threat Score : {total_score}")

    print("-----------------------------------")


# ==========================================================
# Command Frequency
# ==========================================================

def command_frequency(logs):

    commands = Counter(

        log["command"]

        for log in logs
    )

    print("\n======= Command Frequency =======\n")

    for command, count in commands.most_common():

        print(

            f"{command:<35}"

            f"{count}"
        )


# ==========================================================
# Dashboard
# ==========================================================

def dashboard(logs):

    unique_ips = {

        log["ip"]

        for log in logs
    }

    attacks = Counter(

        log["attack_type"]

        for log in logs
    )

    commands = Counter(

        log["command"]

        for log in logs
    )

    print("\n========== Dashboard ==========\n")

    print(f"Total Logs        : {len(logs)}")

    print(f"Unique IPs        : {len(unique_ips)}")

    print(f"Attack Types      : {len(attacks)}")

    if attacks:

        print(

            f"Most Common Attack: "

            f"{attacks.most_common(1)[0][0]}"
        )

    if commands:

        print(

            f"Most Common Command: "

            f"{commands.most_common(1)[0][0]}"
        )

    print()


# ==========================================================
# Future AI Placeholder
# ==========================================================

def ai_anomaly_detection():
    """
    Placeholder.

    Future:
    - AI-based anomaly detection
    - Behaviour analytics
    - Predictive threat modelling
    """
    pass


# ==========================================================
# Future Export Placeholder
# ==========================================================

def export_report():
    """
    Placeholder.

    Future:
    - Export JSON
    - Export CSV
    - Export PDF
    """
    pass


# ==========================================================
# CLI Menu
# ==========================================================

def menu():

    while True:

        logs = load_logs()

        print("""

=========================================
       XYNERA Honeypot Log Viewer
=========================================

1. Show Latest Logs
2. Search by IP
3. Search by Attack Type
4. Search by Severity
5. Threat Score Summary
6. Command Frequency
7. Dashboard
8. Exit

=========================================
""")

        choice = input("Select Option: ")

        if choice == "1":

            latest_logs(logs)

        elif choice == "2":

            filter_ip(logs)

        elif choice == "3":

            filter_attack(logs)

        elif choice == "4":

            filter_severity(logs)

        elif choice == "5":

            threat_summary(logs)

        elif choice == "6":

            command_frequency(logs)

        elif choice == "7":

            dashboard(logs)

        elif choice == "8":

            print("\nGoodbye.\n")

            break

        else:

            print("\nInvalid Choice.\n")


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    menu()