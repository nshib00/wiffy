import json
import logging
import re
from os import getenv
from pathlib import Path

from dotenv import find_dotenv, load_dotenv, set_key
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


envfile = find_dotenv()
load_dotenv(envfile)


def format_to_win_path_string(string: str) -> str:
    for sym in "/:*?»<>|":
        if sym in string:
            string = string.replace(sym, "")
    filename_parts = string.split(".")
    if len(filename_parts) > 2:
        string = string.replace(".", "", len(filename_parts) - 2)
    return string


def format_url_string(url_string: str) -> str:
    return url_string.replace('/', '-').replace('(', '').replace(')', '').replace('\'', '-')


def create_driver() -> webdriver.chrome.webdriver.WebDriver:
    driver_options = Options()
    driver_options.add_extension("D:\projects\wiffy\chromedriver\extensions\AdBlocker-Ultimate.crx")
    driver_service = Service(executable_path="D:\projects\wiffy\chromedriver\chromedriver-win64\chromedriver.exe")
    driver = webdriver.Chrome(options=driver_options, service=driver_service)
    driver.maximize_window()
    return driver


def save_vk_user_id(user_id: str):
    set_key(envfile, 'VK_USER_ID', user_id)


def get_user_id_regex() -> re.Pattern:
    return re.compile(r"^(?!\d{3,})[a-z0-9._]{2,29}")


def check_long_underscores_in_user_id(user_id: str) -> None:
    underscores_in_row = 0
    for symbol in user_id:
        if symbol == '_':
            underscores_in_row += 1
        else:
            underscores_in_row = 0
        if underscores_in_row == 2:
            raise ValueError('VK user ID cannot contain double (or more long) underscore.')


def are_symbols_after_dots_correct_in_user_id(user_id: str) -> bool:
    symbols_after_dot = 0
    for index, symbol in enumerate(user_id):
        if symbol == '.':
            for index2, symbol2 in enumerate(user_id[index+1:]):
                if symbol2 == '.':
                    symbols_after_dot = 0
                else:
                    if index2 == index + 1:
                        if symbol2.isalpha():
                            symbols_after_dot += 1
                        else:
                            return False
                    else:
                        symbols_after_dot += 1
            if symbols_after_dot < 4:
                return False
    return True


def user_id_is_correct(user_id: str) -> bool:
    check_long_underscores_in_user_id(user_id)
    are_dots_correct = are_symbols_after_dots_correct_in_user_id(user_id)
    return not user_id.startswith('_') and not user_id.endswith('_') and are_dots_correct


def get_logger(logger_filename: str, filemode="a") -> logging.Logger:
    Path("logs").mkdir(exist_ok=True)
    logger = logging.getLogger(__name__)
    logger_format = "(%(name)s) %(asctime)s [%(levelname)s] function: %(funcName)s | %(message)s"
    logging.basicConfig(
        filename=f"logs/{logger_filename}",
        level=logging.INFO,
        format=logger_format,
        filemode=filemode,
    )
    return logger


def count_saved_tracks() -> int:
    tracks_count = 0
    with open("songs_data.json", encoding="utf-8") as file:
        songs_data_from_file = json.load(file)
    for song_page in songs_data_from_file:
        tracks_count += len(song_page.get('songs'))
    return tracks_count


def get_default_download_path() -> str:
    default_download_path_obj = Path("~/Downloads/wiffy")
    return str(default_download_path_obj.expanduser())


def change_download_path(new_path: str) -> None:
    if Path(new_path).is_dir():
        set_key(envfile, "DOWNLOAD_PATH", new_path)
    else:
        set_key(envfile, "DOWNLOAD_PATH", get_default_download_path())


def get_download_path() -> str:
    return getenv("DOWNLOAD_PATH")


def calls_counter(func):
    def wrapper(*args, **kwargs):
        if func.__name__ == "download_song":
            wrapper.count += 1
        return func(*args, **kwargs)

    wrapper.count = 0
    return wrapper
