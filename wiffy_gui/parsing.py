import requests
from selenium.common import WebDriverException

from utils.logger import get_gui_logger
from wiffy_gui.items.labels import WiffyTextLabel
from wiffy_parser.core import parse

logger = get_gui_logger()


def start_tracks_parsing(info_label: WiffyTextLabel) -> None:
    info_label.clear()
    info_label.configure(text="Getting data about tracks from VK page...")
    try:
        requests.get("https://kissvk.com")
        parse()
    except requests.ConnectionError as e:
        info_label.configure(
            text="No internet connection. To find tracks from VK,\nyou need to connect to internet and try again.",
            text_color="red",
        )
        logger.error(f"{e.__class__.__name__}: {e}")
    except WebDriverException as e:
        info_label.configure(
            text="Parser exception occured.\nProbably, the page didn't load "
            "in time because of slow\ninternet connection.",
            text_color="red",
        )
        logger.error(f"{e.__class__.__name__}: {e}")
    except Exception as e:
        info_label.configure(text=f"Error occured: {e.__class__.__name__}.", text_color="red")
        logger.error(f"{e.__class__.__name__}: {e}")
    else:
        info_label.configure(
            text='Tracks from VK found succesfully.\nYou can click the "Show found tracks" button to check it.',
            text_color="green",
        )
