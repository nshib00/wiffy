from bs4 import BeautifulSoup

from utils.logger import get_logger

logger = get_logger(__name__)


def save_html_in_file(pages_html: list[str]) -> None:
    soup = BeautifulSoup(parser="lxml")
    soup.append(soup.new_tag("html"))
    soup.html.append(soup.new_tag("body"))
    for page in pages_html:
        soup.body.extend(BeautifulSoup(page, "lxml").body)
    with open("source.html", "w", encoding="utf-8") as file:
        file.write(str(soup.prettify()))


def get_song_cards() -> list:
    logger.info("Getting track elements from the web page...")
    with open("source.html", encoding="utf-8") as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")
    trs = [
        tr for tr in soup.find_all("tr") if tr.attrs.get("ng-repeat") is not None
    ]  # ng-repeat: "song in songs | limitTo:13:0"
    return trs
