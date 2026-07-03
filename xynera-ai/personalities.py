PERSONALITIES = {
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
    # New Personalities - Thursday Task
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


def get_personality(ip=None, attack_type=None, score=0):
    """Dynamic Persona Management"""
    if score >= 35 or (attack_type and "suspicion" in str(attack_type).lower()):
        return PERSONALITIES["highvalue"]
    elif score >= 20 or (attack_type and ("nmap" in str(attack_type).lower() or "wget" in str(attack_type).lower())):
        return PERSONALITIES["developer"]
    elif score >= 15:
        return PERSONALITIES["corporate"]
    elif score >= 10:
        return PERSONALITIES["banking"]
    elif score <= 6:
        return PERSONALITIES["newbie"]
    else:
        return PERSONALITIES["default"]
