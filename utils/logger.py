import logging
from pathlib import Path


def get_logger(logger_filename: str, filemode="a") -> logging.Logger:
    Path("logs").mkdir(exist_ok=True)
    logger = logging.getLogger(__name__)
    logger_format = "(%(name)s) %(asctime)s [%(levelname)s] function: %(funcName)s | %(message)s"
    logging.basicConfig(
        filename=f"logs/{logger_filename}.log",
        level=logging.INFO,
        format=logger_format,
        filemode=filemode,
    )
    return logger
