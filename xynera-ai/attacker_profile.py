profiles = {}

SCORES = {
    "Reconnaissance": 2,
    "Malware Download Attempt": 7,
    "Permission Manipulation": 5,
    "Reverse Shell Attempt": 10,
    "Unknown": 1
}


def update_profile(ip, attack_type, command):

    if ip not in profiles:
        profiles[ip] = {
            "commands": [],
            "score": 0
        }

    profiles[ip]["commands"].append(command)

    score = SCORES.get(attack_type, 1)

    profiles[ip]["score"] += score

    return profiles[ip]["score"]
