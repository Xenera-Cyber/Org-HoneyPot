import logging
from config import LOG_FILE

logger = logging.getLogger("xynera")

logger.setLevel(logging.INFO)

handler = logging.FileHandler(LOG_FILE)

formatter = logging.Formatter(
    "%(asctime)s - %(message)s"
)

handler.setFormatter(formatter)

logger.addHandler(handler)


def log_event(message):
    logger.info(message)
