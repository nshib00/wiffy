from os import getenv
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from fake_useragent import UserAgent
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import utils
from exceptions import TracksNotFoundError


load_dotenv()

logger = utils.get_logger("parser.log", filemode="w")


headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "user-agent": UserAgent().random,
}


def save_html_in_file(pages_html: list[str]) -> None:
    soup = BeautifulSoup(parser="lxml")
    soup.append(soup.new_tag("html"))
    soup.html.append(soup.new_tag("body"))
    for page in pages_html:
        soup.body.extend(BeautifulSoup(page, "lxml").body)
    with open("source.html", "w", encoding="utf-8") as file:
        file.write(str(soup.prettify()))


def get_source_page(driver: WebDriver) -> None:
    pages_html = []
    page_num = 1
    next_page_btn_xpath = "/html/body/div[6]/div/div[3]/div[3]/p[2]/button[2]"
    wait = WebDriverWait(driver, timeout=30)
    while True:
        try:
            next_page_btn = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, next_page_btn_xpath)
                )
            )
            next_page_btn.click()
            pages_html.append(driver.page_source)
            page_num += 1
        except TimeoutException:
            popup = wait.until(
                EC.visibility_of_element_located(
                    (By.ID, 'shareModal')
                )
            )
            close_btn = popup.find_element(By.CLASS_NAME, 'close')
            close_btn.click()
            continue
        except Exception as e:
            logger.error(f'Exception occured: {e.__class__.__name__}: {e}')
            break
        finally:
            save_html_in_file(pages_html)


def get_song_cards() -> list:
    logger.info("Getting track elements from the web page...")
    with open("source.html", encoding="utf-8") as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")
    trs = [tr for tr in soup.find_all("tr") if tr.attrs.get("ng-repeat") is not None]
    return trs


def save_songs_data(song_cards: list) -> None:
    tracks_count = 0
    logger.info("Gettings tracks data...")
    with open("songs_data.txt", "w", encoding="utf-8") as file:
        for i, song_card in enumerate(song_cards, start=1):
            if song_card.find("div", "kvk-title") is None:
                continue
            else:
                tracks_count += 1
                song_title = song_card.find("div", "kvk-title").text.strip()
                song_artist = song_card.find("div", "kvk-artist").text.strip()
                song_ref = song_card.find("a", "btn-outline-primary").attrs.get("href")
                if song_ref is None:
                    song_ref = ""
                else:
                    song_ref = "https:" + song_ref
                song_data = f"{song_artist} - {song_title} | {song_ref}\n"
                file.write(song_data)
    logger.info(f"Tracks found: {tracks_count}")


def kissvk_auth(driver: WebDriver) -> None:
    wait = WebDriverWait(driver, timeout=10)
    auth_btn = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "btn.btn-success.btn-lg"))
    )
    auth_btn.click()
    login_input = wait.until(
        EC.presence_of_element_located((By.NAME, 'login'))
    )
    login_input.clear()
    login_input.send_keys(getenv("VK_LOGIN"))
    login_input.send_keys(Keys.ENTER)
    pwd_input = wait.until(
        EC.presence_of_element_located((By.NAME, 'password'))
    )
    pwd_input.clear()
    pwd_input.send_keys(str(utils.get_pwd()))
    pwd_input.send_keys(Keys.ENTER)


def close_popup_window(driver: WebDriver) -> None:
    main_window, popup_window = driver.window_handles
    driver.switch_to.window(popup_window)
    driver.close()
    driver.switch_to.window(main_window)


def parse() -> None:
    driver = utils.create_driver()
    try:
        driver.get("https://kissvk.com/")
        close_popup_window(driver)
        kissvk_auth(driver)
    except ElementNotInteractableException as e:
        close_btn = driver.find_element(By.CLASS_NAME, 'close')
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


def make_songs_data_dict(count: int | None = None) -> list[dict]:
    with open("songs_data.txt", encoding="utf-8") as file:
        filestrs = file.readlines()
    if count is None:
        needed_songs_count = len(filestrs)
    else:
        needed_songs_count = count
    songs_data = [
        {"title": song_str.split(" | ")[0], "url": song_str.split(" | ")[1]}
        for song_str in filestrs[:needed_songs_count]
    ]
    return songs_data


def make_download_path() -> Path:
    if getenv("DOWNLOAD_PATH") is not None:
        download_path = Path(getenv("DOWNLOAD_PATH"))
    else:
        download_path = Path("~/Downloads/wiffy")
    if not download_path.is_dir():
        download_path.mkdir(exist_ok=True, parents=True)
    return download_path


def download_song(song: dict, download_path: Path) -> None:
    filename = utils.format_to_win_path_string(string=song["title"])
    song_path = download_path / f"{filename}.mp3"

    if not song_path.is_file():
        response = requests.get(song["url"], headers=headers)
        with open(song_path, "wb") as audio:
            audio.write(response.content)
            logger.info(f'Track "{song["title"]}" downloaded successfully.')
    else:
        logger.info(f'Track "{song["title"]}" already exists.')


@utils.calls_counter
def download_songs(songs_count: int | None = None) -> None:
    download_songs.downloaded_songs_count = 0
    logger.info(f"Downloading tracks: {songs_count}.")
    if songs_count is None:
        songs_data = make_songs_data_dict()
    else:
        songs_data = make_songs_data_dict(count=songs_count)
    if not songs_data:
        raise TracksNotFoundError
    download_path = make_download_path()
    for index, song in enumerate(songs_data, start=1):
        download_song(song, download_path)
        download_songs.downloaded_songs_count += 1
    logger.info("Tracks downloading ended.")


def get_saved_songs_info() -> tuple[str, int]:
    songs_str = ""
    with open("songs_data.txt", encoding="utf-8") as file:
        songs_info_list = file.readlines()
    for index, songstr in enumerate(songs_info_list, start=1):
        song_title = songstr.split(" | ")[0]
        songs_str += f"{index}) {song_title}\n"
    return songs_str, len(songs_info_list)
