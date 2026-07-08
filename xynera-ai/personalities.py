PERSONALITIES = {
    # New Threat-level based Personas
    "friendly": {
        "name": "Friendly Server",
        "hostname": "friendly-srv",
        "user": "support",
        "style": "friendly",
        "description": "Helpful and polite, behaves like an unhardened server with welcoming banners",
        "response_style": "helpful, overly polite, returns detailed and welcoming system messages"
    },
    "normal": {
        "name": "Normal Server",
        "hostname": "ubuntu-server",
        "user": "ubuntu",
        "style": "normal",
        "description": "Standard production server",
        "response_style": "standard, professional, clean terminal output"
    },
    "suspicious": {
        "name": "Suspicious Server",
        "hostname": "corp-internal-secure",
        "user": "sysadmin",
        "style": "suspicious",
        "description": "Cautious, alert, prints occasional warning banners",
        "response_style": "cautious, alert, prints occasional warning banners or security notices, returns slightly defensive output"
    },
    "high_security": {
        "name": "High Security Server",
        "hostname": "prod-restricted-01",
        "user": "root",
        "style": "high_security",
        "description": "Highly restrictive, hardened, logs everything, simulates auditing",
        "response_style": "highly restrictive, extremely secure, logs every command, returns minimal details, denies access to sensitive areas, simulates auditing logs"
    },

    # Backwards Compatible Personas
    "default": {
        "name": "Standard Ubuntu Server",
        "hostname": "ubuntu-server",
        "user": "ubuntu",
        "style": "professional",
        "description": "Clean production server",
        "response_style": "concise, accurate, and professional"
    },
    "newbie": {
        "name": "Home Lab Server",
        "hostname": "nupur-pc",
        "user": "nupur",
        "style": "casual",
        "description": "Beginner user's personal machine",
        "response_style": "verbose, friendly, with small mistakes"
    },
    "developer": {
        "name": "Developer Workstation",
        "hostname": "dev-xynera",
        "user": "dev",
        "style": "techy",
        "description": "Full development environment",
        "response_style": "technical, shows docker, git, python, node.js"
    },
    "highvalue": {
        "name": "High Value Corporate Server",
        "hostname": "prod-finance-01",
        "user": "admin",
        "style": "strict",
        "description": "Banking / Corporate production server",
        "response_style": "very cautious, professional, minimal information"
    },
    "corporate": {
        "name": "Corporate Enterprise Server",
        "hostname": "corp-mail-01",
        "user": "sysadmin",
        "style": "formal",
        "description": "Large company internal server",
        "response_style": "professional, mentions policies and monitoring"
    },
    "banking": {
        "name": "Banking Production Server",
        "hostname": "core-banking-02",
        "user": "dba",
        "style": "secure",
        "description": "Financial institution server",
        "response_style": "highly secure, logs everything, very careful"
    },
    "university": {
        "name": "University Research Server",
        "hostname": "research-lab-05",
        "user": "student",
        "style": "academic",
        "description": "Academic research environment",
        "response_style": "educational tone, mentions research tools"
    },
    "cloud": {
        "name": "Cloud Infrastructure Server",
        "hostname": "aws-prod-234",
        "user": "ec2-user",
        "style": "cloud",
        "description": "AWS / Cloud production instance",
        "response_style": "mentions cloud services, kubernetes, docker"
    }
}

HIGHVALUE_THRESHOLD = 35
DEVELOPER_THRESHOLD = 20
CORPORATE_THRESHOLD = 15
BANKING_THRESHOLD = 10
NEWBIE_THRESHOLD = 6

HIGHVALUE_ATTACKS = (
    "suspicion",
    "privilege",
    "exploit",
)

DEVELOPER_ATTACKS = (
    "nmap",
    "wget",
    "curl",
    "git",
    "python",
)

CLOUD_ATTACKS = (
    "aws",
    "docker",
    "kubernetes",
    "kubectl",
    "cloud",
)

UNIVERSITY_ATTACKS = (
    "research",
    "university",
    "academic",
    "student",
    "lab",
)


def get_personality(profile=None, threat_score=None, ip=None, attack_type=None, score=0):
    # Check if called using the new signature: get_personality(profile, threat_score)
    if isinstance(profile, dict) and threat_score is not None:
        level = "LOW"
        score_val = 0
        if isinstance(threat_score, dict):
            level = threat_score.get("risk_level") or threat_score.get("threat_level", "LOW")
            score_val = threat_score.get("score") or threat_score.get("final_score", 0)
        elif isinstance(threat_score, (int, float)):
            score_val = threat_score
            if score_val >= 70:
                level = "CRITICAL"
            elif score_val >= 45:
                level = "HIGH"
            elif score_val >= 25:
                level = "MEDIUM"
            else:
                level = "LOW"

        if level == "CRITICAL" or score_val >= 70:
            return PERSONALITIES["high_security"]
        elif level == "HIGH" or score_val >= 45:
            return PERSONALITIES["suspicious"]
        elif level == "MEDIUM" or score_val >= 25:
            return PERSONALITIES["normal"]
        else:
            return PERSONALITIES["friendly"]

    # Fallback to old behavior for backward compatibility (ip, attack_type, score)
    resolved_ip = ip
    resolved_attack_type = attack_type
    resolved_score = score

    if isinstance(profile, str):
        resolved_ip = profile
        if isinstance(threat_score, str):
            resolved_attack_type = threat_score
            if isinstance(ip, (int, float)):
                resolved_score = ip
        elif isinstance(threat_score, (int, float)):
            resolved_score = threat_score

    attack = str(resolved_attack_type).lower() if resolved_attack_type else ""

    if (
        resolved_score >= HIGHVALUE_THRESHOLD
        or any(keyword in attack for keyword in HIGHVALUE_ATTACKS)
    ):
        return PERSONALITIES["highvalue"]

    if any(keyword in attack for keyword in CLOUD_ATTACKS):
        return PERSONALITIES["cloud"]

    if any(keyword in attack for keyword in UNIVERSITY_ATTACKS):
        return PERSONALITIES["university"]

    if (
        resolved_score >= DEVELOPER_THRESHOLD
        or any(keyword in attack for keyword in DEVELOPER_ATTACKS)
    ):
        return PERSONALITIES["developer"]

    if resolved_score >= CORPORATE_THRESHOLD:
        return PERSONALITIES["corporate"]

    if resolved_score >= BANKING_THRESHOLD:
        return PERSONALITIES["banking"]

    if resolved_score <= NEWBIE_THRESHOLD:
        return PERSONALITIES["newbie"]

    return PERSONALITIES["default"]
