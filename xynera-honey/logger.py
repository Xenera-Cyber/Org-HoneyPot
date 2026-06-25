import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

LOG_DIR = "logs"

LOG_FILE = os.path.join(
    LOG_DIR,
    "attacks.log"
)

MAX_BYTES = 5 * 1024 * 1024
BACKUP_COUNT = 3


def setup_logger():

    os.makedirs(
        LOG_DIR,
        exist_ok=True
    )

    logger = logging.getLogger(
        "attack_logger"
    )

    logger.setLevel(
        logging.INFO
    )

    if logger.handlers:
        return logger

    handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=MAX_BYTES,
        backupCount=BACKUP_COUNT,
        encoding="utf-8"
    )

    handler.setFormatter(
        logging.Formatter("%(message)s")
    )

    logger.addHandler(
        handler
    )

    # Write the table header only once
    if not os.path.exists(LOG_FILE) or os.path.getsize(LOG_FILE) == 0:
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write(
                f"{'Timestamp':<22}"
                f"{'IP':<18}"
                f"{'Command':<18}"
                f"{'Attack Type':<25}"
                f"{'Score'}\n"
            )
            f.write("-" * 95 + "\n")

    return logger


_logger = setup_logger()


ATTACK_SCORES = {
    "Reconnaissance": 20,
    "Directory Navigation": 10,
    "Credential Enumeration": 60,
    "Malware Download": 90,
    "Malware Preparation": 95,
    "Malware Execution": 100,
    "Privilege Escalation": 95,
    "Destructive Attack": 100,
    "Unknown": 5
}


def log_command(
    command,
    attack_type,
    ip_address="UNKNOWN",
    session_id="NO-SESSION",
    severity="INFO"
):

    score = ATTACK_SCORES.get(
        attack_type,
        5
    )

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log = (
        f"{timestamp:<22}"
        f"{ip_address:<18}"
        f"{command:<18}"
        f"{attack_type:<25}"
        f"{score}"
    )

    level = getattr(
        logging,
        severity.upper(),
        logging.INFO
    )

    _logger.log(
        level,
        log
    )