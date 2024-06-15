def count_saved_tracks() -> int:
    tracks_count = 0
    for _ in open("songs_data.txt", encoding="utf-8"):
        tracks_count += 1
    return tracks_count


def calls_counter(func):
    def wrapper(*args, **kwargs):
        if func.__name__ == "download_song":
            wrapper.count += 1
        return func(*args, **kwargs)

    wrapper.count = 0
    return wrapper