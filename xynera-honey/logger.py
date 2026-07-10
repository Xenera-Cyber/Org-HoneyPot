import os
import logging
from logging.handlers import RotatingFileHandler

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "attacks.log")
MAX_BYTES = 5 * 1024 * 1024
BACKUP_COUNT = 3

ATTACK_SCORES = {
    "Reconnaissance": 20,
    "Directory Navigation": 10,
    "Credential Enumeration": 60,
    "Malware Download": 90,
    "Malware Preparation": 95,
    "Malware Execution": 100,
    "File Transfer": 80,
    "Privilege Escalation": 95,
    "Lateral Movement": 80,
    "Destructive Attack": 100,
    "Reverse Shell Activity": 100,
    "Unknown": 5,
}


def setup_logger():
    os.makedirs(LOG_DIR, exist_ok=True)
    logger = logging.getLogger("attack_logger")
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=MAX_BYTES,
        backupCount=BACKUP_COUNT,
        encoding="utf-8"
    )
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


_logger = setup_logger()


def log_command(
    command,
    attack_type,
    ip_address="UNKNOWN",
    session_id="NO-SESSION",
    severity="INFO"
):
    score = ATTACK_SCORES.get(attack_type, 5)
    level = getattr(
        logging,
        severity.upper(),
        logging.INFO
    )

    message = (
        f"IP={ip_address} | "
        f"SESSION={session_id} | "
        f"TYPE={attack_type} | "
        f"SCORE={score} | "
        f"CMD={command}"
    )

    _logger.log(level, message)