import os
import logging
from logging.handlers import RotatingFileHandler
from attack_analyzer import SHARED_ATTACK_SCORES

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "attacks.log")
MAX_BYTES = 5 * 1024 * 1024
BACKUP_COUNT = 3


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
    # Uses the shared dictionary
    score = SHARED_ATTACK_SCORES.get(attack_type, 5)
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


# ==========================================================
# AI Threat Synchronization -- additional log line
# ==========================================================
def log_ai_prediction(
    command,
    ip_address="UNKNOWN",
    session_id="NO-SESSION",
    ai_attack_type="Unknown",
    prediction=None,
    severity="INFO"
):
    """
    Logs the AI backend's own attack-type read and/or threat prediction
    for a command as a SEPARATE log line, tagged SOURCE=AI.

    This is purely additive: it never calls, wraps, or modifies
    log_command() above, so the existing local-classifier log line for
    the same command (TYPE=..., SCORE=...) is untouched. Keeping the two
    as distinct, clearly-tagged lines lets an analyst compare the local
    and AI signals for the same command side by side in attacks.log
    instead of one overwriting the other.
    """
    level = getattr(
        logging,
        severity.upper(),
        logging.INFO
    )
    message = (
        f"IP={ip_address} | "
        f"SESSION={session_id} | "
        f"SOURCE=AI | "
        f"AI_TYPE={ai_attack_type} | "
        f"PREDICTION={prediction} | "
        f"CMD={command}"
    )
    _logger.log(level, message)