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


def get_personality(ip=None, attack_type=None, score=0):
    attack = str(attack_type).lower() if attack_type else ""

    if (
        score >= HIGHVALUE_THRESHOLD
        or any(keyword in attack for keyword in HIGHVALUE_ATTACKS)
    ):
        return PERSONALITIES["highvalue"]

    if any(keyword in attack for keyword in CLOUD_ATTACKS):
        return PERSONALITIES["cloud"]

    if any(keyword in attack for keyword in UNIVERSITY_ATTACKS):
        return PERSONALITIES["university"]

    if (
        score >= DEVELOPER_THRESHOLD
        or any(keyword in attack for keyword in DEVELOPER_ATTACKS)
    ):
        return PERSONALITIES["developer"]

    if score >= CORPORATE_THRESHOLD:
        return PERSONALITIES["corporate"]

    if score >= BANKING_THRESHOLD:
        return PERSONALITIES["banking"]

    if score <= NEWBIE_THRESHOLD:
        return PERSONALITIES["newbie"]

    return PERSONALITIES["default"]
