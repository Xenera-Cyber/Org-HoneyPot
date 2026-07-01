import json
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


def calculate_curiosity_score(
    commands_executed,
    unique_commands,
    directories_visited,
    recon_commands,
    persistence_attempts
):

    score = 0

    score += commands_executed * 2

    score += unique_commands * 3

    score += directories_visited * 2

    score += recon_commands * 5

    score += persistence_attempts * 8

    if score > 100:
        score = 100

    result = {

        "commands_executed": commands_executed,

        "unique_commands": unique_commands,

        "directories_visited": directories_visited,

        "recon_commands": recon_commands,

        "persistence_attempts": persistence_attempts,

        "curiosity_score": score

    }

    return result
def calculate_engagement_score(
    session_duration,
    commands_executed,
    successful_commands,
    failed_commands,
    files_accessed,
    services_accessed
):

    score = 0

    # Session duration
    score += min(session_duration // 2, 20)

    # Commands executed
    score += min(commands_executed * 2, 30)

    # Successful commands
    score += min(successful_commands * 2, 20)

    # Files accessed
    score += min(files_accessed * 2, 15)

    # Services accessed
    score += min(services_accessed * 3, 15)

    if score > 100:
        score = 100

    engagement_level = "LOW"

    if score >= 80:
        engagement_level = "HIGH"
    elif score >= 50:
        engagement_level = "MEDIUM"

    return {
        "session_duration": session_duration,
        "commands_executed": commands_executed,
        "successful_commands": successful_commands,
        "failed_commands": failed_commands,
        "files_accessed": files_accessed,
        "services_accessed": services_accessed,
        "engagement_score": score,
        "engagement_level": engagement_level
    }
if __name__ == "__main__":

    result = calculate_engagement_score(
        session_duration=42,
        commands_executed=18,
        successful_commands=15,
        failed_commands=3,
        files_accessed=9,
        services_accessed=4
    )

    import json
    print(json.dumps(result, indent=4))

if __name__ == "__main__":

    result = calculate_curiosity_score(

        commands_executed=18,

        unique_commands=11,

        directories_visited=7,

        recon_commands=5,

        persistence_attempts=2

    )

    print(json.dumps(result, indent=4))
