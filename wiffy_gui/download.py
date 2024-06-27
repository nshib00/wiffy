from ssl import SSLError

import customtkinter as ctk
from requests import ConnectionError

from exceptions import TracksNotFoundError
from utils.counters import count_saved_tracks
from utils.logger import get_logger
from utils.paths import make_download_path
from wiffy_gui.items.custom import Spinbox
from wiffy_gui.items.labels import WiffyTextLabel
from wiffy_gui.items.progressbar import create_progressbar_elements, grid_progressbar_elements
from wiffy_parser.download import download_song
from wiffy_parser.songs_data import make_songs_data_dict

logger = get_logger(__name__)


def download_songs_with_progressbar(
    pb: ctk.CTkProgressBar, pb_label: WiffyTextLabel, songs_count: int | None = None
) -> None:
    songs_data = make_songs_data_dict(count=songs_count)
    for index, song in enumerate(songs_data, start=1):
        download_path = make_download_path()
        download_song(song, download_path)
        pb.set(value=index / songs_count)
        pb_label.configure(text=f"{index}/{songs_count}")


def start_tracks_downloading(
    info_label: WiffyTextLabel,
    content_frame: ctk.CTkFrame,
    download_frame: ctk.CTkFrame,
    spinbox: Spinbox,
) -> None:
    info_label.configure(text="Downloading tracks...", text_color="#c0c0c0")
    choosed_tracks_count = spinbox.get()
    saved_tracks_count = count_saved_tracks()
    if choosed_tracks_count is None:
        choosed_tracks_count = saved_tracks_count
    download_frame.grid_forget()
    progressbar_frame = ctk.CTkFrame(content_frame, width=360, height=50)
    progressbar, pb_label = create_progressbar_elements(progressbar_frame, songs_count=int(choosed_tracks_count))
    grid_progressbar_elements(pb_frame=progressbar_frame, pb=progressbar, pb_label=pb_label)
    progressbar.set(0)
    try:
        if int(choosed_tracks_count) <= 0:
            raise ValueError(
                "You choose no tracks for download.\n"
                "To download tracks, go back and choose tracks count greater than 0."
            )
        if int(choosed_tracks_count) > saved_tracks_count:
            if saved_tracks_count > 0:
                raise ValueError(f"Incorrect value. Tracks count should be between 1 and {saved_tracks_count}.")
            else:
                raise ValueError("You have no tracks for download. Find tracks and then try again.")
        if choosed_tracks_count is None:
            download_songs_with_progressbar(pb=progressbar, pb_label=pb_label)
        else:
            download_songs_with_progressbar(pb=progressbar, pb_label=pb_label, songs_count=int(choosed_tracks_count))
    except TracksNotFoundError as e:
        info_label.configure(
            text="There are no saved tracks. Before downloading,\nclick on the “Find tracks from VK”"
            "button so that the program saves\ninformation about tracks from your VK page.",
            text_color="red",
        )
        logger.error(f"{e.__class__.__name__}: {e}")
    except ValueError as e:
        info_label.configure(text=e.args[0], text_color="red")
        logger.error(f"{e.__class__.__name__}: {e}")
    except (SSLError, ConnectionError) as e:
        info_label.configure(
            text="Internet connection error.\nPlease, check your internet connection.",
            text_color="red",
        )
        logger.error(f"{e.__class__.__name__}: {e}")
    except Exception as e:
        info_label.configure(text=f"Error occured: {e.__class__.__name__}.", text_color="red")
        logger.error(f"{e.__class__.__name__}: {e}")
    else:
        info_label.configure(text="Tracks downloaded successfully.", text_color="green")
