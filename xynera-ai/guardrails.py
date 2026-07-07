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
    Validates AI-generated responses before returning them
    """

    command = command.lower()

    # Dangerous command protection
    for cmd in BLOCKED_COMMANDS:
        if cmd in command:
            return "[Guardrail] Dangerous command detected. Response blocked."

    # Malware / exploit protection
    for keyword in BLOCKED_KEYWORDS:
        if keyword in command:
            return "[Guardrail] Unsafe security request detected."

    # Empty response protection
    if response is None or response.strip() == "":
        return "[Guardrail] No valid response generated."

    return response
