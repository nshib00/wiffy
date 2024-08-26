import requests
from selenium.common import WebDriverException

from utils.logger import get_gui_logger
from wiffy_gui import text
from wiffy_gui.items.labels import WiffyTextLabel
from wiffy_parser.core import parse

logger = get_gui_logger()


def start_tracks_parsing(info_label: WiffyTextLabel) -> None:
    info_label.clear()
    info_label.configure(text=text.GETTING_TRACKS_DATA_MESSAGE)
    try:
        requests.get("https://kissvk.com")
        parse()
    except requests.ConnectionError as e:
        info_label.configure(
            text=text.NO_INTERNET_CONNECTION_MESSAGE,
            text_color="red",
        )
        logger.error(f"{e.__class__.__name__}: {e}")
    except WebDriverException as e:
        info_label.configure(
            text=text.GENERAL_PARSER_ERROR_MESSAGE,
            text_color="red",
        )
        logger.error(f"{e.__class__.__name__}: {e}")
    except Exception as e:
        info_label.configure(text=f"{text.GENERAL_ERROR_MESSAGE} {e.__class__.__name__}.", text_color="red")
        logger.error(f"{e.__class__.__name__}: {e}")
    else:
        info_label.configure(
            text=text.FIND_SUCCESS_MESSAGE,
            text_color="green",
        )
