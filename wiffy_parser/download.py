from pathlib import Path

import requests
from fake_useragent import UserAgent

from exceptions import TracksNotFoundError
from utils.counters import calls_counter
from utils.formatting import format_to_win_path_string
from utils.logger import get_parser_logger
from utils.paths import make_download_path
from wiffy_parser.songs_data import make_songs_data_dict

logger = get_parser_logger()

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "user-agent": UserAgent().random,
}


def download_song(song: dict, download_path: Path) -> None:
    retries_count = 3
    filename = format_to_win_path_string(string=song["title"])
    song_path = download_path / f"{filename}.mp3"

    """ Скачиваем аудиофайл, если его нет в папке или если аудиофайл пустой. """
    if not song_path.is_file() or song_path.is_file() and song_path.stat().st_size == 0:
        for retry in range(retries_count - 1, -1, -1):  # обратный отсчет ретраев от retries_count до 0
            response = requests.get(song["url"], headers=headers)
            with open(song_path, "wb") as audio:
                audio.write(response.content)
            if song_path.stat().st_size == 0:
                continue
            elif song_path.stat().st_size > 0:
                logger.info(f'Track "{song["title"]}" downloaded successfully.')
                break
        else:
            logger.info(f'Downloading track "{song["title"]}" failed. Retries made: {retries_count}.')
    else:
        logger.info(f'Track "{song["title"]}" already exists.')


@calls_counter
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
    for song in songs_data:
        download_song(song, download_path)
        download_songs.downloaded_songs_count += 1
    logger.info("Tracks downloading ended.")
