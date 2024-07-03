import logging
from pathlib import Path


def create_logger(logger_filename: str) -> logging.Logger:
    Path("logs").mkdir(exist_ok=True)
    logger = logging.getLogger(logger_filename)
    logger_format = "(%(module)s.%(funcName)s) [%(levelname)s] %(asctime)s | %(message)s"
    file_handler = logging.FileHandler(filename=f"logs/{logger_filename}.log", mode="a", encoding="utf-8")
    logging.basicConfig(level=logging.INFO, format=logger_format, handlers=[file_handler])
    return logger


def get_parser_logger() -> logging.Logger:
    return create_logger(logger_filename="wiffy_parser")


def get_gui_logger() -> logging.Logger:
    return create_logger(logger_filename="wiffy_gui")
