"""
deception_engine.py

Purpose:
    Generates deceptive responses based on detected attack types.
    Sits in front of the standard command router (see command_router.py):
    for each command, adapt_response() is consulted first. If it returns
    a value, that value is sent to the attacker instead of the normal
    command output. If it returns None, the command router falls back to
    its regular handling.

Future Architecture:
    - AI-powered adaptive deception
    - RAG-based context retrieval
    - Session-aware deception strategies
    - Threat intelligence integration
"""

import random

import malware_detector


# ==========================================================
# Attacker Intent Profiling
# ==========================================================
def update_profile(command, session):
    """
    Maintain a rolling read on the attacker's apparent intent for this
    session (recon / credential / malware), stored on the session dict
    itself so it never bleeds into other sessions. Currently used for
    session summaries/analytics; attack-type dispatch below remains the
    primary routing signal since it is already derived per-command by
    attack_analyzer.classify().
    """
    profile = session.setdefault("attacker_profile", {"intent": "recon"})
    cmd = command.lower()

    if "/etc/passwd" in cmd or "/etc/shadow" in cmd or "grep" in cmd:
        profile["intent"] = "credential"
    elif "wget" in cmd or "curl" in cmd or cmd.startswith("nc"):
        profile["intent"] = "malware"
    else:
        profile["intent"] = "recon"

    return profile


def get_dynamic_uptime():
    """Randomized uptime so repeated calls don't look scripted/static."""
    days = 37
    hours = random.randint(0, 23)
    minutes = random.randint(0, 59)
    users = random.randint(1, 4)
    load = ", ".join(f"{random.uniform(0.0, 0.5):.2f}" for _ in range(3))
    return (
        f"14:23:{random.randint(0, 59):02d} up {days} days, {hours}:{minutes:02d}, "
        f"{users} users, load average: {load}"
    )


# ==========================================================
# Reconnaissance Deception
# ==========================================================
def reconnaissance_deception(command, session):
    """
    Reconnaissance covers many distinct commands (ls, ps, netstat, ...)
    that already have rich, dedicated simulations in fake_filesystem.py /
    fake_process.py / fake_network.py, so this only special-cases
    "uptime" (which attack_analyzer.classify() does not tag as
    Reconnaissance on its own) and otherwise defers to normal routing.
    """
    if command.strip().lower() == "uptime":
        return get_dynamic_uptime()
    return None


# ==========================================================
# Credential Enumeration Deception
# ==========================================================
def credential_enumeration_deception(command, session):
    """
    /etc/shadow does NOT exist in the simulated filesystem, so without
    this handler an attacker probing for it would get a giveaway
    "No such file" response. This supplies a plausible-looking (but
    useless, hash-free) shadow file instead.

    /etc/passwd DOES exist in fake_filesystem.py's template, but that
    template is static and hardcodes the "ubuntu" account name. Once a
    session has a dynamic identity (see session_manager.py), a static
    file would show a stale username that no longer matches whoami/the
    shell prompt/etc. This override takes precedence over the static
    filesystem entry for /etc/passwd specifically so its content always
    reflects the session's live username (bug fix, Shatakshi).
    """
    if "/etc/shadow" in command:
        return (
            "root:*:19000:0:99999:7:::\n"
            "ubuntu:*:19000:0:99999:7:::\n"
            "dev:*:19000:0:99999:7:::"
        )
    if "/etc/passwd" in command:
        username = session.get("username", "ubuntu")
        return f"""root:x:0:0:root:/root:/bin/bash
{username}:x:1000:1000::/home/{username}:/bin/bash
dev:x:1001:1001::/home/dev:/bin/bash"""
    return None


# ==========================================================
# Malware Download Deception
# ==========================================================
def malware_download_deception(command, session):
    """
    Delegates to malware_detector.py, which already validates the target
    and produces a randomized, believable wget/curl transcript. This
    avoids a second, weaker/static implementation of the same behaviour
    living here.
    """
    cmd = command.strip().lower()
    if cmd.startswith("wget"):
        return malware_detector.handle_wget(command)[0]
    if cmd.startswith("curl"):
        return malware_detector.handle_curl(command)[0]
    return None


# ==========================================================
# Lateral Movement Deception
# ==========================================================
def lateral_movement_deception(command, session):
    """
    fake_network.ssh() already provides a richer, randomized simulation
    (banner, password prompts, occasional connection failures) than a
    single static line would. Deferring to it avoids downgrading that
    existing behaviour.
    """
    return None


# ==========================================================
# Reverse Shell Deception
# ==========================================================
def reverse_shell_deception(command, session):
    """
    Future AI/RAG:
    - Simulate compromised shell
    - Generate believable shell responses
    - Maintain attacker interaction
    """
    return None


# ==========================================================
# Privilege Escalation Deception
# ==========================================================
def privilege_escalation_deception(command, session):
    """
    Future:
    - Fake sudo execution
    - Simulate permission changes
    - AI-generated privilege escalation behaviour
    """
    return None


# ==========================================================
# Default Deception
# ==========================================================
def default_deception(command, session):
    return None


# ==========================================================
# Attack Type Dispatcher
# ==========================================================
DECEPTION_HANDLERS = {
    "Reconnaissance": reconnaissance_deception,
    "Credential Enumeration": credential_enumeration_deception,
    "Malware Download": malware_download_deception,
    "Lateral Movement": lateral_movement_deception,
    "Reverse Shell Activity": reverse_shell_deception,
    "Privilege Escalation": privilege_escalation_deception,
}


# ==========================================================
# Main Deception Engine
# ==========================================================
def adapt_response(command, session, attack_type):
    """
    Routes each detected attack type to its respective deception handler.
    Returns None when no deception applies, signalling the command
    router to fall back to its standard handling for that command.
    """
    update_profile(command, session)

    if attack_type == "Unknown" and command.strip().lower() == "uptime":
        return get_dynamic_uptime()

    handler = DECEPTION_HANDLERS.get(attack_type, default_deception)
    return handler(command, session)


