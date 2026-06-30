def adapt_response(command, session, attack_type):
    history = session.get("commands", [])

    # ===== RECON PHASE =====
    if attack_type == "Reconnaissance":
        # Let AI generate realistic responses
        return None

    # ===== PRIVILEGE ENUMERATION =====
    elif attack_type == "Credential Enumeration":
        if "/etc/passwd" in command:
            return """root:x:0:0:root:/root:/bin/bash
ubuntu:x:1000:1000::/home/ubuntu:/bin/bash
dev:x:1001:1001::/home/dev:/bin/bash"""

    # ===== MALWARE DOWNLOAD =====
    elif attack_type == "Malware Download":
        return """--2026-- Downloading http://malware.sh
Resolving malware.sh... 192.168.1.10
Connecting... connected.
HTTP request sent, awaiting response... 200 OK
Length: 2048 (2.0K) [application/x-sh]
Saving to: 'malware.sh'

malware.sh 100%[==================>] 2.00K --.-KB/s

Download complete."""

    # ===== LATERAL MOVEMENT =====
    elif attack_type == "Lateral Movement":
        return (
            "ssh: connect to host 192.168.1.5 "
            "port 22: Connection timed out"
        )

    # ===== DEFAULT =====
    return None
