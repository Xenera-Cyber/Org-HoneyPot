import json
import time

profiles = {}

SCORES = {
    "Reconnaissance": 2,
    "Malware Download Attempt": 7,
    "Permission Manipulation": 5,
    "Reverse Shell Attempt": 10,
    "SQL Injection Attempt": 8,
    "Defense Evasion": 6,
    "Persistence Creation": 9,
    "Privilege Escalation Attempt": 9,
    "Malware Execution Attempt": 9,
    "Unknown": 1
}


def update_profile(ip, attack_type, command, cwd=None, score=None):
    """
    Updates attacker profile and cumulative score.
    Existing function retained for backward compatibility.
    """

    if ip not in profiles:
        profiles[ip] = {
            "commands": [],
            "score": 0,
            "first_seen": time.time(),
            "last_seen": time.time(),
            "cwd_list": set(),
            "recon_count": 0,
            "persistence_count": 0,
            "successful_count": 0,
            "failed_count": 0,
            "files_accessed": 0,
            "services_accessed": 0
        }

    p = profiles[ip]
    p["commands"].append(command)
    p["last_seen"] = time.time()

    if cwd:
        p["cwd_list"].add(cwd)

    if attack_type == "Reconnaissance":
        p["recon_count"] += 1
    elif attack_type == "Persistence Creation":
        p["persistence_count"] += 1

    cmd_lower = (command or "").lower()
    if any(f_cmd in cmd_lower for f_cmd in ["cat ", "less ", "more ", "tail ", "head ", "nano ", "vi ", "vim "]):
        p["files_accessed"] += 1
    if any(s_cmd in cmd_lower for s_cmd in ["systemctl", "service", "init "]):
        p["services_accessed"] += 1

    if score is not None:
        p["score"] = score
    else:
        score_val = SCORES.get(attack_type, 1)
        p["score"] += score_val

    return p["score"]


def update_profile_response(ip, reply):
    """
    Updates attacker success/failure counts based on the AI response.
    """
    if ip in profiles:
        p = profiles[ip]
        reply_lower = (reply or "").lower()
        if not reply_lower or any(err in reply_lower for err in ["command not found", "permission denied", "blocked"]):
            p["failed_count"] += 1
        else:
            p["successful_count"] += 1


def get_detailed_profile(ip, risk_score, threat_level):
    """
    Generates curiosity, engagement, and behaviour profiles for the attacker.
    """
    if ip not in profiles:
        return {
            "curiosity": {
                "commands_executed": 0,
                "unique_commands": 0,
                "directories_visited": 0,
                "recon_commands": 0,
                "persistence_attempts": 0,
                "curiosity_score": 0
            },
            "engagement": {
                "session_duration": 0,
                "commands_executed": 0,
                "successful_commands": 0,
                "failed_commands": 0,
                "files_accessed": 0,
                "services_accessed": 0,
                "engagement_score": 0,
                "engagement_level": "LOW"
            },
            "behaviour": {
                "Curiosity Score": 0,
                "Persistence Score": "LOW",
                "Interaction Depth": "LOW",
                "Risk Score": risk_score,
                "Session Complexity": "LOW"
            },
            "commands": [],
            "confidence_score": 0.50
        }
    p = profiles[ip]
    session_duration = int(p["last_seen"] - p["first_seen"])
    commands_executed = len(p["commands"])
    unique_commands = len(set(p["commands"]))
    directories_visited = len(p["cwd_list"])
    recon_commands = p["recon_count"]
    persistence_attempts = p["persistence_count"]
    successful_commands = p["successful_count"]
    failed_commands = p["failed_count"]
    files_accessed = p["files_accessed"]
    services_accessed = p["services_accessed"]

    curiosity = calculate_curiosity_score(
        commands_executed=commands_executed,
        unique_commands=unique_commands,
        directories_visited=directories_visited,
        recon_commands=recon_commands,
        persistence_attempts=persistence_attempts
    )

    engagement = calculate_engagement_score(
        session_duration=session_duration,
        commands_executed=commands_executed,
        successful_commands=successful_commands,
        failed_commands=failed_commands,
        files_accessed=files_accessed,
        services_accessed=services_accessed
    )

    behaviour = generate_behaviour_profile(
        curiosity_score=curiosity["curiosity_score"],
        persistence_attempts=persistence_attempts,
        interaction_depth=directories_visited + unique_commands // 2,
        risk_score=risk_score,
        session_complexity=len(set(p["commands"]))
    )

    profile_confidence = min(0.5 + (len(p["commands"]) * 0.05), 0.99)

    return {
        "curiosity": curiosity,
        "engagement": engagement,
        "behaviour": behaviour,
        "commands": p["commands"],
        "confidence_score": round(profile_confidence, 2)
    }


def calculate_curiosity_score(
    commands_executed,
    unique_commands,
    directories_visited,
    recon_commands,
    persistence_attempts
):
    """
    Calculates attacker curiosity score.
    """

    score = 0

    score += commands_executed * 2
    score += unique_commands * 3
    score += directories_visited * 2
    score += recon_commands * 5
    score += persistence_attempts * 8

    score = min(score, 100)

    return {
        "commands_executed": commands_executed,
        "unique_commands": unique_commands,
        "directories_visited": directories_visited,
        "recon_commands": recon_commands,
        "persistence_attempts": persistence_attempts,
        "curiosity_score": score
    }


def calculate_engagement_score(
    session_duration,
    commands_executed,
    successful_commands,
    failed_commands,
    files_accessed,
    services_accessed
):
    """
    Calculates attacker engagement score.
    """

    score = 0

    score += min(session_duration // 2, 20)
    score += min(commands_executed * 2, 30)
    score += min(successful_commands * 2, 20)
    score += min(files_accessed * 2, 15)
    score += min(services_accessed * 3, 15)

    score = min(score, 100)

    if score >= 80:
        engagement_level = "HIGH"
    elif score >= 50:
        engagement_level = "MEDIUM"
    else:
        engagement_level = "LOW"

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


def generate_behaviour_profile(
    curiosity_score,
    persistence_attempts,
    interaction_depth,
    risk_score,
    session_complexity
):
    """
    Generates attacker behaviour profile.
    """

    if persistence_attempts >= 5:
        persistence = "HIGH"
    elif persistence_attempts >= 3:
        persistence = "MEDIUM"
    else:
        persistence = "LOW"

    if interaction_depth >= 8:
        interaction = "HIGH"
    elif interaction_depth >= 5:
        interaction = "MEDIUM"
    else:
        interaction = "LOW"

    if session_complexity >= 8:
        complexity = "HIGH"
    elif session_complexity >= 5:
        complexity = "MEDIUM"
    else:
        complexity = "LOW"

    return {
        "Curiosity Score": curiosity_score,
        "Persistence Score": persistence,
        "Interaction Depth": interaction,
        "Risk Score": risk_score,
        "Session Complexity": complexity
    }

session_datasets = {}

def get_session_data(session_id, commands=None):
    if commands is None:
        commands=[]
    
    """
    Generates and caches session-specific dynamic corporate data.
    The seed is derived deterministically from the session_id to maintain consistency
    across multiple commands within the same session.
    """
    if not session_id:
        session_id = "default_session"
        
    import hashlib
    h = hashlib.md5(session_id.encode()).hexdigest()
    seed = int(h, 16) % 100000000
    
    from data_generator import get_generated_all
    # Re-generate/update the dataset so that log files reflect the current command history
    session_datasets[session_id] = get_generated_all(seed=seed, commands=commands)
    return session_datasets[session_id]


if __name__ == "__main__":

    curiosity = calculate_curiosity_score(
        commands_executed=18,
        unique_commands=11,
        directories_visited=7,
        recon_commands=5,
        persistence_attempts=2
    )

    print("\n===== Curiosity Score =====")
    print(json.dumps(curiosity, indent=4))
    engagement = calculate_engagement_score(
    session_duration=30,
    commands_executed=18,
    successful_commands=15,
    failed_commands=3,
    files_accessed=6,
    services_accessed=2
    )

    print("\n===== Engagement Score =====")
    print(json.dumps(engagement, indent=4))
    behaviour = generate_behaviour_profile(
    curiosity_score=curiosity["curiosity_score"],
    persistence_attempts=3,
    interaction_depth=8,
    risk_score=82,
    session_complexity=7
    )

    print("\n===== Behaviour Profile =====")
    print(json.dumps(behaviour, indent=4))
