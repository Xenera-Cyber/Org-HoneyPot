"""
guardrails.py
Model Safety & Guardrails for Xynera Honeypot
"""

BLOCKED_COMMANDS = [
    "rm -rf",
    "mkfs",
    "dd if=",
    "shutdown",
    "reboot",
    "poweroff",
    "halt",
    "init 0"
]

BLOCKED_KEYWORDS = [
    "ransomware",
    "keylogger",
    "malware",
    "exploit",
    "payload",
    "reverse shell",
    "meterpreter"
]


def apply_guardrails(command, response):
    """
    Validates commands and AI-generated responses
    before sending them to the attacker.

    This function is intentionally kept backward-compatible
    with the main branch.
    """

    # Safely handle None commands
    command = (command or "").lower()

    # Dangerous command protection
    for blocked_command in BLOCKED_COMMANDS:
        if blocked_command in command:
            return "[Guardrail] Dangerous command detected. Response blocked."

    # Malware / exploit protection
    for keyword in BLOCKED_KEYWORDS:
        if keyword in command:
            return "[Guardrail] Unsafe security request detected."

    # Empty response protection
    if not str(response).strip():
        return "[Guardrail] No valid response generated."

    return response


if __name__ == "__main__":

    print(
        apply_guardrails(
            "sudo rm -rf /",
            "Deleting..."
        )
    )

    print(
        apply_guardrails(
            "ls -la",
            "Directory listing..."
        )
    )

    print(
        apply_guardrails(
            None,
            ""
        )
    )