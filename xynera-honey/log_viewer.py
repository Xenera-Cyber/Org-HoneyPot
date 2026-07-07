import re
import csv
import json
from collections import Counter
from datetime import datetime

import matplotlib.pyplot as plt

from attack_analyzer import threat_score

# ==========================================================
# Log File Configuration
# ==========================================================
LOG_FILE = "logs/attacks.log"
JSON_LOG_FILE = "logs/attacks.json"

# ==========================================================
# Log Parser
# ==========================================================
# Matches logger.py's log_command() output:
# [timestamp] [LEVEL] IP=... | SESSION=... | TYPE=... | SCORE=... | CMD=...
LOG_PATTERN = re.compile(
    r"\[(.*?)\]\s"
    r"\[(.*?)\]\s"
    r"IP=(.*?)\s\|\s"
    r"SESSION=(.*?)\s\|\s"
    r"TYPE=(.*?)\s\|\s"
    r"SCORE=(.*?)\s\|\s"
    r"CMD=(.*)"
)


# ==========================================================
# Load Text Logs
# ==========================================================
def load_logs():
    """Load attack logs from attacks.log."""
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
                    "score": match.group(6),
                    "command": match.group(7)
                })
    except FileNotFoundError:
        print("\nText log file not found.\n")
    return logs


# ==========================================================
# Load JSON Logs
# ==========================================================
def load_json_logs():
    """
    Load logs from attacks.json.
    Expected format:
    [
        {
            "timestamp": "...",
            "severity": "...",
            "ip": "...",
            "session": "...",
            "attack_type": "...",
            "command": "..."
        }
    ]
    """
    try:
        with open(JSON_LOG_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            print("\nInvalid JSON format.\n")
            return []
    except FileNotFoundError:
        print("\nJSON log file not found.\n")
        return []
    except json.JSONDecodeError:
        print("\nInvalid JSON file.\n")
        return []


# ==========================================================
# Display Utilities
# ==========================================================
def print_logs(logs):
    """Print logs in a readable format."""
    if not logs:
        print("\nNo matching logs found.\n")
        return
    for log in logs:
        print("=" * 80)
        print(f"Timestamp : {log['timestamp']}")
        print(f"Severity  : {log['severity']}")
        print(f"IP        : {log['ip']}")
        print(f"Session   : {log['session']}")
        print(f"Attack    : {log['attack_type']}")
        print(f"Command   : {log['command']}")
    print("=" * 80)


def print_table(logs):
    """Compact table view."""
    if not logs:
        print("\nNo logs available.\n")
        return
    print()
    print(
        f"{'Timestamp':<20}"
        f"{'IP':<18}"
        f"{'Attack Type':<28}"
        f"Command"
    )
    print("-" * 100)
    for log in logs:
        print(
            f"{log['timestamp']:<20}"
            f"{log['ip']:<18}"
            f"{log['attack_type']:<28}"
            f"{log['command']}"
        )
    print()


# ==========================================================
# Helper Utilities
# ==========================================================
def parse_timestamp(timestamp):
    """Convert timestamp string into datetime object."""
    try:
        return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    except Exception:
        return datetime.min


def pause():
    """Wait for user input."""
    input("\nPress Enter to continue...")


# ==========================================================
# Latest Logs
# ==========================================================
def latest_logs(logs):
    """Display the latest N log entries."""
    if not logs:
        print("\nNo logs available.\n")
        return
    try:
        n = int(input("\nNumber of latest logs: "))
    except ValueError:
        print("\nInvalid input.\n")
        return
    print_logs(logs[-n:])


# ==========================================================
# Filter by IP
# ==========================================================
def filter_ip(logs):
    """Search logs by attacker IP."""
    ip = input("\nEnter IP Address: ").strip()
    result = [log for log in logs if log["ip"] == ip]
    print_logs(result)


# ==========================================================
# Filter by Attack Type
# ==========================================================
def filter_attack(logs):
    """Search logs by attack type."""
    attack = input("\nEnter Attack Type: ").strip().lower()
    result = [log for log in logs if log["attack_type"].lower() == attack]
    print_logs(result)


# ==========================================================
# Filter by Severity
# ==========================================================
def filter_severity(logs):
    """Search logs by severity."""
    severity = input("\nEnter Severity: ").strip().upper()
    result = [log for log in logs if log["severity"].upper() == severity]
    print_logs(result)


# ==========================================================
# Session-wise Logs
# ==========================================================
def session_logs(logs):
    """Display all logs for a session."""
    session = input("\nEnter Session ID: ").strip()
    result = [log for log in logs if log["session"] == session]
    print_logs(result)


# ==========================================================
# Timeline View
# ==========================================================
def timeline_view(logs):
    """Display logs in chronological order."""
    if not logs:
        print("\nNo logs available.\n")
        return
    ordered_logs = sorted(logs, key=lambda log: parse_timestamp(log["timestamp"]))
    print("\n========== Timeline ==========\n")
    for log in ordered_logs:
        print(
            f"{log['timestamp']}"
            f" | "
            f"{log['ip']}"
            f" | "
            f"{log['attack_type']}"
            f" | "
            f"{log['command']}"
        )


# ==========================================================
# Search by Command
# ==========================================================
def search_command(logs):
    """Search logs by command."""
    keyword = input("\nEnter command keyword: ").strip().lower()
    result = [log for log in logs if keyword in log["command"].lower()]
    print_logs(result)


# ==========================================================
# Search by Time Range
# ==========================================================
def search_time_range(logs):
    """
    Search logs within a time range.
    Format: YYYY-MM-DD HH:MM:SS
    """
    print()
    start = input("Start Time : ").strip()
    end = input("End Time   : ").strip()
    try:
        start_time = parse_timestamp(start)
        end_time = parse_timestamp(end)
    except Exception:
        print("\nInvalid timestamp.\n")
        return
    result = [
        log for log in logs
        if start_time <= parse_timestamp(log["timestamp"]) <= end_time
    ]
    print_logs(result)


# ==========================================================
# Sort Logs
# ==========================================================
def sort_logs(logs):
    """Display logs sorted by timestamp."""
    ordered = sorted(
        logs,
        key=lambda log: parse_timestamp(log["timestamp"]),
        reverse=True
    )
    print_logs(ordered)


# ==========================================================
# Threat Score Summary
# ==========================================================
def threat_summary(logs):
    """Display threat score summary."""
    if not logs:
        print("\nNo logs available.\n")
        return
    attack_counter = Counter()
    total_score = 0
    for log in logs:
        attack = log["attack_type"]
        attack_counter[attack] += 1
        total_score += threat_score(attack)

    print("\n========== Threat Summary ==========\n")
    print(f"{'Attack Type':<30}{'Count':<10}{'Threat Score'}")
    print("-" * 60)
    for attack, count in attack_counter.items():
        score = threat_score(attack)
        print(f"{attack:<30}{count:<10}{score * count}")
    print("-" * 60)
    print(f"Overall Threat Score : {total_score}")
    print()


# ==========================================================
# Command Frequency
# ==========================================================
def command_frequency(logs):
    """Display command usage frequency."""
    if not logs:
        print("\nNo logs available.\n")
        return
    commands = Counter(log["command"] for log in logs)
    print("\n========== Command Frequency ==========\n")
    print(f"{'Command':<45}Count")
    print("-" * 60)
    for command, count in commands.most_common():
        print(f"{command:<45}{count}")
    print()


# ==========================================================
# Top Attackers
# ==========================================================
def top_attackers(logs):
    """Display attackers ranked by activity."""
    if not logs:
        print("\nNo logs available.\n")
        return
    attackers = Counter(log["ip"] for log in logs)
    print("\n========== Top Attackers ==========\n")
    print(f"{'IP Address':<25}Commands")
    print("-" * 40)
    for ip, count in attackers.most_common():
        print(f"{ip:<25}{count}")
    print()


# ==========================================================
# Dashboard
# ==========================================================
def dashboard(logs):
    """Quick dashboard."""
    if not logs:
        print("\nNo logs available.\n")
        return
    attack_counter = Counter(log["attack_type"] for log in logs)
    command_counter = Counter(log["command"] for log in logs)
    ip_counter = Counter(log["ip"] for log in logs)

    print("\n========== Dashboard ==========\n")
    print(f"Total Logs           : {len(logs)}")
    print(f"Unique IPs           : {len(ip_counter)}")
    print(f"Attack Types         : {len(attack_counter)}")
    print(f"Unique Commands      : {len(command_counter)}")
    print(f"Top Attacker         : {ip_counter.most_common(1)[0][0]}")
    print(f"Most Common Attack   : {attack_counter.most_common(1)[0][0]}")
    print(f"Most Common Command  : {command_counter.most_common(1)[0][0]}")
    print()


# ==========================================================
# Advanced Statistics
# ==========================================================
def statistics(logs):
    """Display log statistics."""
    if not logs:
        print("\nNo logs available.\n")
        return
    attack_counter = Counter(log["attack_type"] for log in logs)
    severity_counter = Counter(log["severity"] for log in logs)
    session_counter = Counter(log["session"] for log in logs)
    ip_counter = Counter(log["ip"] for log in logs)
    total_score = sum(threat_score(log["attack_type"]) for log in logs)
    average_score = total_score / len(logs)

    print("\n========== Statistics ==========\n")
    print(f"Total Logs           : {len(logs)}")
    print(f"Unique Sessions      : {len(session_counter)}")
    print(f"Unique IPs           : {len(ip_counter)}")
    print(f"Attack Types         : {len(attack_counter)}")
    print(f"Severity Levels      : {len(severity_counter)}")
    print(f"Average Threat Score : {average_score:.2f}")
    print(f"Overall Threat Score : {total_score}")
    print()

    print("Attack Distribution")
    print("-------------------")
    for attack, count in attack_counter.items():
        print(f"{attack:<30}{count}")
    print()

    print("Severity Distribution")
    print("---------------------")
    for severity, count in severity_counter.items():
        print(f"{severity:<20}{count}")
    print()

    print("Top 5 Commands")
    print("--------------")
    command_counter = Counter(log["command"] for log in logs)
    for command, count in command_counter.most_common(5):
        print(f"{command:<45}{count}")
    print()


# ==========================================================
# Attack Distribution Graph
# ==========================================================
def attack_distribution_graph(logs):
    """Display attack type distribution."""
    if not logs:
        print("\nNo logs available.\n")
        return
    attacks = Counter(log["attack_type"] for log in logs)
    plt.figure(figsize=(10, 6))
    plt.bar(attacks.keys(), attacks.values())
    plt.title("Attack Type Distribution")
    plt.xlabel("Attack Type")
    plt.ylabel("Count")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.show()


# ==========================================================
# Severity Distribution Graph
# ==========================================================
def severity_distribution_graph(logs):
    """Display severity distribution."""
    if not logs:
        print("\nNo logs available.\n")
        return
    severity = Counter(log["severity"] for log in logs)
    plt.figure(figsize=(8, 6))
    plt.pie(severity.values(), labels=severity.keys(), autopct="%1.1f%%", startangle=90)
    plt.title("Severity Distribution")
    plt.tight_layout()
    plt.show()


# ==========================================================
# Top Attackers Graph
# ==========================================================
def top_attackers_graph(logs):
    """Display top attacker graph."""
    if not logs:
        print("\nNo logs available.\n")
        return
    attackers = Counter(log["ip"] for log in logs)
    top = attackers.most_common(10)
    ips = [ip for ip, _ in top]
    counts = [count for _, count in top]
    plt.figure(figsize=(10, 6))
    plt.bar(ips, counts)
    plt.title("Top Attackers")
    plt.xlabel("IP Address")
    plt.ylabel("Commands")
    plt.xticks(rotation=25)
    plt.tight_layout()
    plt.show()


# ==========================================================
# Threat Score Trend
# ==========================================================
def threat_score_graph(logs):
    """Display cumulative threat score."""
    if not logs:
        print("\nNo logs available.\n")
        return
    score = 0
    cumulative = []
    x = []
    for index, log in enumerate(logs):
        score += threat_score(log["attack_type"])
        cumulative.append(score)
        x.append(index + 1)
    plt.figure(figsize=(10, 6))
    plt.plot(x, cumulative, marker="o")
    plt.title("Threat Score Trend")
    plt.xlabel("Log Entry")
    plt.ylabel("Cumulative Threat Score")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# ==========================================================
# Command Frequency Graph
# ==========================================================
def command_frequency_graph(logs):
    """Display top commands graph."""
    if not logs:
        print("\nNo logs available.\n")
        return
    commands = Counter(log["command"] for log in logs)
    top = commands.most_common(10)
    names = [command for command, _ in top]
    counts = [count for _, count in top]
    plt.figure(figsize=(12, 6))
    plt.bar(names, counts)
    plt.title("Most Executed Commands")
    plt.xlabel("Command")
    plt.ylabel("Frequency")
    plt.xticks(rotation=35)
    plt.tight_layout()
    plt.show()


# ==========================================================
# Timeline Graph
# ==========================================================
def timeline_graph(logs):
    """Timeline of attack activity."""
    if not logs:
        print("\nNo logs available.\n")
        return
    ordered = sorted(logs, key=lambda log: parse_timestamp(log["timestamp"]))
    x = list(range(len(ordered)))
    y = [threat_score(log["attack_type"]) for log in ordered]
    plt.figure(figsize=(12, 6))
    plt.plot(x, y, marker="o")
    plt.title("Attack Timeline")
    plt.xlabel("Timeline")
    plt.ylabel("Threat Score")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# ==========================================================
# Analytics Dashboard
# ==========================================================
def analytics_dashboard(logs):
    """Run all analytics."""
    while True:
        print("""
==============================
    Analytics Dashboard
==============================
1. Attack Distribution
2. Severity Distribution
3. Top Attackers
4. Threat Score Trend
5. Command Frequency
6. Timeline View
7. Back
==============================
""")
        choice = input("Select Option: ")
        if choice == "1":
            attack_distribution_graph(logs)
        elif choice == "2":
            severity_distribution_graph(logs)
        elif choice == "3":
            top_attackers_graph(logs)
        elif choice == "4":
            threat_score_graph(logs)
        elif choice == "5":
            command_frequency_graph(logs)
        elif choice == "6":
            timeline_graph(logs)
        elif choice == "7":
            break
        else:
            print("\nInvalid Choice.\n")


# ==========================================================
# Export Logs to JSON
# ==========================================================
def export_json(logs):
    """Export parsed logs to JSON."""
    filename = input("\nOutput JSON filename (default: report.json): ").strip()
    if not filename:
        filename = "report.json"
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(logs, file, indent=4)
    print(f"\nJSON report saved as {filename}\n")


# ==========================================================
# Export Logs to CSV
# ==========================================================
def export_csv(logs):
    """Export logs to CSV."""
    filename = input("\nOutput CSV filename (default: report.csv): ").strip()
    if not filename:
        filename = "report.csv"
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Timestamp", "Severity", "IP", "Session", "Attack Type", "Command"
        ])
        for log in logs:
            writer.writerow([
                log["timestamp"],
                log["severity"],
                log["ip"],
                log["session"],
                log["attack_type"],
                log["command"]
            ])
    print(f"\nCSV report saved as {filename}\n")


# ==========================================================
# Session Statistics
# ==========================================================
def session_statistics(logs):
    """Statistics grouped by session."""
    sessions = {}
    for log in logs:
        sid = log["session"]
        if sid not in sessions:
            sessions[sid] = {"commands": 0, "score": 0, "attacks": Counter()}
        sessions[sid]["commands"] += 1
        sessions[sid]["score"] += threat_score(log["attack_type"])
        sessions[sid]["attacks"][log["attack_type"]] += 1

    print("\n========== Session Statistics ==========\n")
    for sid, info in sessions.items():
        print("-" * 60)
        print(f"Session : {sid}")
        print(f"Commands: {info['commands']}")
        print(f"Threat Score: {info['score']}")
        print("Attack Types:")
        for attack, count in info["attacks"].items():
            print(f"   {attack:<30}{count}")


# ==========================================================
# IP Intelligence Summary
# ==========================================================
def ip_intelligence(logs):
    """Statistics grouped by attacker IP."""
    attackers = {}
    for log in logs:
        ip = log["ip"]
        if ip not in attackers:
            attackers[ip] = {"commands": 0, "score": 0, "sessions": set()}
        attackers[ip]["commands"] += 1
        attackers[ip]["score"] += threat_score(log["attack_type"])
        attackers[ip]["sessions"].add(log["session"])

    print("\n========== IP Intelligence ==========\n")
    for ip, info in attackers.items():
        print("-" * 60)
        print(f"IP Address : {ip}")
        print(f"Commands   : {info['commands']}")
        print(f"Sessions   : {len(info['sessions'])}")
        print(f"Threat Score : {info['score']}")


# ==========================================================
# Generate Report
# ==========================================================
def generate_report(logs):
    """Overall summary report."""
    print("\n========== Honeypot Report ==========\n")
    dashboard(logs)
    print()
    statistics(logs)
    print()
    threat_summary(logs)


# ==========================================================
# AI Anomaly Detection Placeholder
# ==========================================================
def ai_anomaly_detection(logs):
    """
    Future AI Integration:
    ----------------------
    - Detect unusual attacker behaviour
    - Behaviour clustering
    - ML-based anomaly scoring
    - Predict attack progression
    - Alert generation
    """
    print("\n[Future Feature] AI Anomaly Detection")


# ==========================================================
# RAG Context Retrieval Placeholder
# ==========================================================
def rag_context_lookup(logs):
    """
    Future:
        Retrieve similar attacks from vector database
        for analyst support.
    """
    print("\n[Future Feature] RAG Context Lookup")


# ==========================================================
# Threat Intelligence Placeholder
# ==========================================================
def threat_intelligence(logs):
    """
    Future:
    - VirusTotal lookup
    - AbuseIPDB lookup
    - GeoIP lookup
    - IOC enrichment
    """
    print("\n[Future Feature] Threat Intelligence")


# ==========================================================
# Main CLI Menu
# ==========================================================
def menu():
    while True:
        logs = load_logs()
        print("""
====================================================
           XYNERA Honeypot Log Viewer
====================================================
 Log Viewer
 -----------------------------
1. Show Latest Logs
2. Search by IP
3. Search by Attack Type
4. Search by Severity
5. Search by Command
6. Search by Time Range
7. Session-wise Logs
8. Timeline View
 Analytics
 -----------------------------
9. Threat Score Summary
10. Command Frequency
11. Top Attackers
12. Dashboard
13. Statistics
14. Graph Analytics Dashboard
 Reports
 -----------------------------
15. Export JSON
16. Export CSV
17. Generate Summary Report
 Intelligence
 -----------------------------
18. IP Intelligence
19. Session Statistics
 Future Features
 -----------------------------
20. AI Anomaly Detection
21. RAG Context Lookup
22. Threat Intelligence
23. Load JSON Logs
24. Exit
====================================================
""")
        choice = input("Select Option : ").strip()

        if choice == "1":
            latest_logs(logs)
        elif choice == "2":
            filter_ip(logs)
        elif choice == "3":
            filter_attack(logs)
        elif choice == "4":
            filter_severity(logs)
        elif choice == "5":
            search_command(logs)
        elif choice == "6":
            search_time_range(logs)
        elif choice == "7":
            session_logs(logs)
        elif choice == "8":
            timeline_view(logs)
        elif choice == "9":
            threat_summary(logs)
        elif choice == "10":
            command_frequency(logs)
        elif choice == "11":
            top_attackers(logs)
        elif choice == "12":
            dashboard(logs)
        elif choice == "13":
            statistics(logs)
        elif choice == "14":
            analytics_dashboard(logs)
        elif choice == "15":
            export_json(logs)
        elif choice == "16":
            export_csv(logs)
        elif choice == "17":
            generate_report(logs)
        elif choice == "18":
            ip_intelligence(logs)
        elif choice == "19":
            session_statistics(logs)
        elif choice == "20":
            ai_anomaly_detection(logs)
        elif choice == "21":
            rag_context_lookup(logs)
        elif choice == "22":
            threat_intelligence(logs)
        elif choice == "23":
            json_logs = load_json_logs()
            print_logs(json_logs)
        elif choice == "24":
            print("\nGoodbye.\n")
            break
        else:
            print("\nInvalid Choice.\n")

        pause()


# ==========================================================
# Main
# ==========================================================
if __name__ == "__main__":
    menu()