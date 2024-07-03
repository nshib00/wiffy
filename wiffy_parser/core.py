from dotenv import load_dotenv
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By

from utils.logger import get_parser_logger
from wiffy_parser.html import get_song_cards
from wiffy_parser.selenium import close_popup_window, create_driver, get_source_page, kissvk_auth
from wiffy_parser.songs_data import save_songs_data

load_dotenv()

logger = get_parser_logger()


def parse() -> None:
    driver = create_driver()
    try:
        driver.get("https://kissvk.com/")
        close_popup_window(driver)
        kissvk_auth(driver)
    except ElementNotInteractableException as e:
        close_btn = driver.find_element(By.CLASS_NAME, "close")
        close_btn.click()
        logger.warning(e)
    except Exception as e:
        logger.error(f"{e.__class__.__name__}: {e}")
    finally:
        get_source_page(driver)
        song_cards = get_song_cards()
        if song_cards:
            save_songs_data(song_cards)
        driver.close()
        driver.quit()
