"""Logging setup: writes to both a log file and the console."""
import logging
import os


def setup_logger(log_file="logs/app.log", level="INFO"):
    os.makedirs(os.path.dirname(log_file) or ".", exist_ok=True)
    logger = logging.getLogger("sis")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    if not logger.handlers:  # avoid duplicate handlers on re-import
        fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(fmt)
        logger.addHandler(file_handler)
        # Console shows only warnings/errors so the menu stays clean.
        console = logging.StreamHandler()
        console.setLevel(logging.WARNING)
        console.setFormatter(fmt)
        logger.addHandler(console)
    return logger
