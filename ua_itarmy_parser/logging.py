"""File to log some info."""
from datetime import datetime
from logging import (
    CRITICAL,
    DEBUG,
    ERROR,
    INFO,
    WARNING,
    Formatter,
    Logger,
    StreamHandler,
    basicConfig,
    getLogger,
)
from os import environ
from pathlib import Path
from re import sub

# Base dir, same to folder where ``README.md``.
# Absolute path, but not hard-coded.
BASE_DIR: Path = Path(__file__).parent.parent


def init_logger() -> Logger:
    """Initialise logger system.

    Also configuring telethon logger, because by default it doesn't print
    anything. Even errors.

    Returns:
        Configured ``Logger`` object.
    """
    log_level = {
        "debug": DEBUG,
        "info": INFO,
        "warning": WARNING,
        "error": ERROR,
        "critical": CRITICAL,
    }[environ.get("ITARMY_LOG_LEVEL", "info").lower()]

    str_time = sub(r"\D", "_", str(datetime.now())[:-7])
    logs_path: Path = Path(BASE_DIR / environ.get("ITARMY_LOG_PATH", "logs")).resolve()
    logs_path.mkdir(exist_ok=True)
    logs_path: str = str(logs_path / (str_time + ".log"))

    basicConfig(level=log_level, filename=logs_path)

    logger = getLogger("ua_itarmy_parser")
    telethon_logger = getLogger()

    handler = StreamHandler()
    handler.setLevel(log_level)
    telethon_handler = StreamHandler()
    telethon_handler.setLevel(ERROR)

    formatter = Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    telethon_formatter = Formatter("%(asctime)s [%(levelname)s] %(message)s")
    telethon_handler.setFormatter(telethon_formatter)

    logger.addHandler(handler)
    telethon_logger.addHandler(telethon_handler)

    return logger


log: Logger = init_logger()
log.debug("Logger configured")
