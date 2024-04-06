import json
from os import getenv
from pathlib import Path

import requests
from dotenv import load_dotenv
from fake_useragent import UserAgent
from requests import Response
from profilehooks import profile

import utils
from songs_classes import Song, SongsHint


load_dotenv()

logger = utils.get_logger("parser.log", filemode="w")

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "user-agent": UserAgent().random,
}

songs_hint = SongsHint(value='')


def build_request_url(url: str, params: dict[str, str]) -> str:
    request_url = url + '?'
    for par_name, par_value in params.items():
        request_url += f'{par_name}={par_value}&'
    return request_url[:-1]


def get_vk_user_id(user_shortname: str) -> int:
    user_id_request = requests.get(
        url=build_request_url(
            'https://api.vk.com/method/users.get',
            params={
                'user_ids': user_shortname,
                'access_token': getenv('VK_ACCESS_TOKEN'),
                'v': '5.191',
            }
        ),
        headers=headers
    )
    return user_id_request.json().get('response')[0].get('id')


def get_songs_data_from_page(user_id: int, page: int) -> json:
    songs_request = requests.get(
        url=build_request_url(
            f'https://i129.kissvk.com/api/song/user/get_songs/{user_id}',
            params={
                'origin': 'kissvk.com',
                'page': page,
                'songs_hint': songs_hint.value,
            }
        ),
        headers=headers
    )
    return songs_request.json()


def save_songs_data(songs_data: list[dict]) -> None:
    logger.info("Saving tracks data...")
    with open("songs_data.json", "w", encoding="utf-8") as file:
        json.dump(songs_data, file, ensure_ascii=False, indent=4)
    logger.info("Songs data saved successfully.")


def get_songs_data() -> list[dict]:
    vk_user_id = get_vk_user_id('nshib')
    page_num = 0
    all_songs_data = []
    while True:
        songs_data_from_page = get_songs_data_from_page(user_id=vk_user_id, page=page_num)
        if page_num == 0:
            songs_hint.value = songs_data_from_page.get('hint')
        if not songs_data_from_page.get('songs'):
            break
        all_songs_data.append(songs_data_from_page)
        page_num += 1
    return all_songs_data


def make_songs_request_url_to_server(server_index: int) -> str:
    return f'https://i{server_index}.kissvk.com/api/song/download/get/11'


def get_url_params_dict(song: Song) -> dict:
    return {
            'origin': 'kissvk.com',
            'url': song.url,
            'artist': utils.format_url_string(song.artist),
            'title': utils.format_url_string(song.title),
            'index': song.index,
            'user_id': 358241846,
            'ui_version': 230706080202,
            'future_urls': 'sid%3A%2F%2F296739633_456241388_e61e5e061e392fbc5d_4c78d33e65d88457f1%2Csid%3A%2F%2F296739633_456241387_15b8916550d4b54e72_086cf6e8327f85bcdb%2Csid%3A%2F%2F296739633_456241386_312c8f04a4189488b4_e20cd05dcb08f4342c%2Csid%3A%2F%2F296739633_456241385_7f50b272c578492a55_477f181c356b535d7c%2Csid%3A%2F%2F296739633_456241384_462e8acdab6e4ea9e6_b45ffdc93a0b1dceaf%2Csid%3A%2F%2F296739633_456241383_1f8ce51410f449f59a_819865da91ec517a63%2Csid%3A%2F%2F296739633_456241382_05a1ec3f4a6044b18c_856e279a8543a3a5b1%2Csid%3A%2F%2F296739633_456241381_a26b0f9dd3a698067d_1661b5b5e8e1015477%2Csid%3A%2F%2F296739633_456241380_1fe8d2dff835b3a086_d1255f21d201acfdbe'
        }


def get_search_response(session: requests.Session, song: Song, server_index: int) -> Response:
    api_method_url = make_songs_request_url_to_server(server_index)
    song_url = build_request_url(
        url=f'{api_method_url}/{utils.format_url_string(song.full_title)}--kissvk.com.mp3',
        params=get_url_params_dict(song)
    )
    request_headers = {}
    response = session.get(song_url, headers=request_headers)
    return response


# def check_cached_server(song_for_request: Song):
#     with open('info.json') as file:
#         cached_kissvk_server_index = json.load()['cached_kissvk_server']
#     response = get_search_response(song=song_for_request, server_index=cached_kissvk_server_index)
#     if response.ok and response.content:
#         logger.info(f'Checking server {server_index}... Success.')
#         return server_index

@profile(stdout=False, filename='profiles/server_search.prof')
def find_available_kissvk_server(song_for_request: Song) -> int:
    with requests.Session() as session:
        for server_index in range(114, 130):
            response = get_search_response(session=session, song=song_for_request, server_index=server_index)
            if response.ok and response.content:
                logger.info(f'Checking server {server_index}... Success.')
                return server_index
            else:
                logger.info(f'Checking server {server_index}... Failed. {response.status_code=}')
    return 0


def request_song_download(song: Song, server_code: int) -> Response | None:
    api_method_url = make_songs_request_url_to_server(server_index=server_code)
    song_url = build_request_url(
        url=f'{api_method_url}/{song.full_title}--kissvk.com.mp3',
        params=get_url_params_dict(song)
    )
    response = requests.get(song_url)
    logger.info(f'server={server_code} -> {response.content=}')
    if response.content is not None:
        return response


def parse() -> None:
    songs_data = get_songs_data()
    save_songs_data(songs_data)


def get_saved_songs_data() -> list[Song]:
    songs_data = []
    with open("songs_data.json", encoding="utf-8") as file:
        songs_data_from_file = json.load(file)
    for song_page in songs_data_from_file:
        for song in song_page.get('songs'):
            songs_data.append(
                Song(
                    artist=song['artist'],
                    title=song['title'],
                    url=song['url'],
                    index=song['index']
                )
            )
    return songs_data


def make_song_objects_list(count: int) -> list[Song]:
    songs_data = get_saved_songs_data()
    return songs_data[:count]


def make_download_path() -> Path:
    if getenv("DOWNLOAD_PATH") is not None:
        download_path = Path(getenv("DOWNLOAD_PATH"))
    else:
        download_path = Path("~/Downloads/wiffy")
    if not download_path.is_dir():
        download_path.mkdir(exist_ok=True, parents=True)
    return download_path


def download_song(song: Song, song_index: int, download_path: Path, server_code: int) -> None:
    filename = utils.format_to_win_path_string(string=song.full_title)
    song_path = download_path / f"{filename}.mp3"

    if not song_path.is_file():
        song_response = request_song_download(song=song, server_code=server_code)
        if not song_response.content:
            logger.warning(f'Track "{song.full_title}" found but download failed.')
        else:
            with open(song_path, "wb") as audio:
                audio.write(song_response.content)
                logger.info(f'Track "{song.full_title}" downloaded successfully.')
    else:
        logger.info(f'Track "{song.full_title}" already exists.')


def make_show_songs_text() -> tuple[str, int]:
    songs_str = ""
    songs_count = 0
    songs_data_list = get_saved_songs_data()
    for song in songs_data_list:
        songs_count += 1
        songs_str += f"{songs_count}) {song.full_title}\n"
    return songs_str, songs_count
