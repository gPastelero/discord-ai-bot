import logging
from logging.handlers import RotatingFileHandler

LOG_PATH = "logs/bot.log"
MAX_BYTES = 5 * 1024 * 1024  # 5 MB per file before rotating
BACKUP_COUNT = 3              # keep at most 3 old log files (~20 MB total)

def setup_logger(name: str = "bot") -> logging.Logger:
    logger = logging.getLogger(name)

    # getLogger returns the same instance for the same name, so guard against
    # adding duplicate handlers if this function is called more than once.
    if logger.handlers:
        return logger

    # Root level is DEBUG so handlers can each filter to their own level.
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # File handler — writes everything (DEBUG+) to a rotating log file.
    file_handler = RotatingFileHandler(
        LOG_PATH, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Console handler — only INFO+ to keep terminal output readable.
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
