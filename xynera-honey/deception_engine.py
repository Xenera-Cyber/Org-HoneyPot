"""
deception_engine.py

Purpose:
    Generates deceptive responses based on detected attack types.

Future Architecture:
    - AI-powered adaptive deception
    - RAG-based context retrieval
    - Session-aware deception strategies
    - Threat intelligence integration
"""

# ==========================================================
# Reconnaissance Deception
# ==========================================================
def reconnaissance_deception(command, session):
    """
    Future AI/RAG:
    - Analyze attacker reconnaissance behaviour
    - Generate adaptive system responses
    - Simulate realistic infrastructure discovery
    """
    return None


# ==========================================================
# Credential Enumeration Deception
# ==========================================================
def credential_enumeration_deception(command, session):
    """
<<<<<<< HEAD
    Bug fix: this previously hardcoded a fake /etc/passwd file listing
    "ubuntu" as the second user account, regardless of the session's
    actual identity. If the AI backend (or anything else) changes the
    session's username/hostname mid-session, this file would still show
    the old, stale "ubuntu" account -- another form of duplicate/
    inconsistent identity storage. It now reads the live username from
    the session dict, same as every other identity-aware command.
    """
=======
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
>>>>>>> origin/hriday/baseline-v3.3
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
    return """--2026-- Downloading http://malware.sh
Resolving malware.sh... 192.168.1.10
Connecting... connected.
HTTP request sent, awaiting response... 200 OK
Length: 2048 (2.0K) [application/x-sh]
Saving to: 'malware.sh'
malware.sh        100%[==================>] 2.00K  --.-KB/s
Download complete."""


# ==========================================================
# Lateral Movement Deception
# ==========================================================
def lateral_movement_deception(command, session):
    return (
        "ssh: connect to host "
        "192.168.1.5 port 22: "
        "Connection timed out"
    )


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
    """
    handler = DECEPTION_HANDLERS.get(attack_type, default_deception)
    return handler(command, session)


