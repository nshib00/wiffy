import base64
import getpass
import logging
import re
from os import getenv
from random import randint
from time import sleep

import keyring
from dotenv import find_dotenv, load_dotenv, set_key
from get_chrome_driver import GetChromeDriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from pathlib import Path


envfile = find_dotenv()
load_dotenv(envfile)


def get_logger(logger_filename: str, filemode="a") -> logging.Logger:
    Path("logs").mkdir(exist_ok=True)
    logger = logging.getLogger(logger_filename)
    logger_format = "(%(name)s) %(asctime)s [%(levelname)s] function: %(funcName)s | %(message)s"
    logging.basicConfig(
        filename=f"logs/{logger_filename}",
        level=logging.INFO,
        format=logger_format,
        filemode=filemode,
    )
    return logger


logger = get_logger('utils.log')


def randsleep(from_: float, to: float) -> None:
    """
    Stops the program execution on random time (from 'from_' to 'to' seconds).
    """

    rand1 = randint(int(from_), int(to))
    if rand1 == int(to):
        rand2 = randint(0, int(to))
    else:
        rand2 = randint(0, 9)
    sleep_time = rand1 + rand2 / 10
    sleep(sleep_time)


def format_to_win_path_string(string: str) -> str:
    for sym in "/:*?»\"<>|!":
        if sym in string:
            string = string.replace(sym, "")
    filename_parts = string.split(".")
    if len(filename_parts) > 2:
        string = string.replace(".", "", len(filename_parts) - 2)
    return string


def clear_folder(path: Path) -> None:
    for sub in path.glob('*/**'):
        if 'extensions' not in str(sub):
            sub.rmdir() if sub.is_dir() else sub.unlink()


def is_driver_need_to_update() -> bool:
    getdriver_obj = GetChromeDriver()
    stable_version_number: str = getdriver_obj.stable_version().split('.')[0]
    downloaded_version_number: str = getenv('DRIVER_VERSION').split('.')[0]
    return int(stable_version_number) != int(downloaded_version_number)


def update_driver() -> None:
    logger.info(f'Driver is need to be updated. Updating driver...')
    getdriver_obj = GetChromeDriver()
    driver_path_str = 'chromedriver'
    chromedriver_path = Path(driver_path_str)
    clear_folder(chromedriver_path)
    getdriver_obj.download_stable_version(output_path=driver_path_str, extract=True)
    save_driver_version_info(version_info=getdriver_obj.stable_version())
    logger.info(f'Driver updated successfully to version {getdriver_obj.stable_version()}.')


def save_driver_version_info(version_info: str) -> None:
    set_key(envfile, 'DRIVER_VERSION', version_info)


def create_driver() -> webdriver.chrome.webdriver.WebDriver:
    driver_options = Options()
    driver_options.add_extension("chromedriver/extensions/AdBlocker-Ultimate.crx")
    driver_service = Service(executable_path="chromedriver/chromedriver.exe")
    logger.info(f'{is_driver_need_to_update()=}')
    if is_driver_need_to_update():
        update_driver()
    driver = webdriver.Chrome(options=driver_options, service=driver_service)
    driver.maximize_window()
    return driver


def save_vk_login(login: str) -> None:
    set_key(envfile, "VK_LOGIN", login)


def get_email_regex() -> re.Pattern:
    return re.compile(r"([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+)")


def get_phone_number_regex() -> re.Pattern:
    return re.compile(r"^((8|\+\d{1,3})[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$")


def string_is_email(string: str) -> bool:
    return (
        "@" in string or re.search(r"\.\s+", string) is not None or re.search(r"[A-Za-z]+", string) is not None
    ) and not string.isdigit()


def set_pwd(pwd_string) -> None:
    keyring.set_password(
        service_name="wiffy_pwd",
        username=getpass.getuser(),
        password=base64.b64decode(pwd_string).decode("utf-8"),
    )


def get_pwd() -> str:
    return keyring.get_password(service_name="wiffy_pwd", username=getpass.getuser())


def count_saved_tracks() -> int:
    tracks_count = 0
    for _ in open("songs_data.txt", encoding="utf-8"):
        tracks_count += 1
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
