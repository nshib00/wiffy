from utils.logger import get_parser_logger

logger = get_parser_logger()


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


def get_saved_songs_info() -> tuple[str, int]:
    songs_str = ""
    with open("songs_data.txt", encoding="utf-8") as file:
        songs_info_list = file.readlines()
    for index, songstr in enumerate(songs_info_list, start=1):
        song_title = songstr.split(" | ")[0]
        songs_str += f"{index}) {song_title}\n"
    return songs_str, len(songs_info_list)


def save_songs_data(song_cards: list) -> None:
    tracks_count = 0
    logger.info("Gettings tracks data...")
    with open("songs_data.txt", "w", encoding="utf-8") as file:
        for song_card in song_cards:
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
