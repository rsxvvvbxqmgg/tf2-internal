import logging
import sys

_FMT = "[%(asctime)s] [%(name)s] %(levelname)s: %(message)s"


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(f"tf2internal.{name}")
    if not logger.handlers:
        h = logging.StreamHandler(sys.stdout)
        h.setFormatter(logging.Formatter(_FMT, datefmt="%H:%M:%S"))
        logger.addHandler(h)
        logger.setLevel(logging.INFO)
    return logger