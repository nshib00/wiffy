from threading import Thread

import customtkinter as ctk

from utils.paths import get_default_download_path, get_download_path
from utils.threads import run_thread
from wiffy_gui.config import app_settings
from wiffy_gui.download import start_tracks_downloading
from wiffy_gui.items.custom import Spinbox
from wiffy_gui.items.labels import WiffyTextLabel
from wiffy_gui.layout.dir_menu import configure_dir_label, open_change_dir_menu


def create_download_frame_widgets(download_frame: ctk.CTkFrame) -> dict:
    download_path = get_download_path() or get_default_download_path()

    tracks_info_label = WiffyTextLabel(download_frame, text="Tracks to download:")
    spinbox = Spinbox(download_frame, width=120)
    info_dir_label = WiffyTextLabel(download_frame, text="Current download folder:")
    current_dir_label = WiffyTextLabel(download_frame, text=download_path)
    change_dir_button = ctk.CTkButton(download_frame, text="Change", font=app_settings.base_font)
    apply_button = ctk.CTkButton(download_frame, text="Apply and download", font=app_settings.base_font)
    return {
        "tracks_info_label": tracks_info_label,
        "spinbox": spinbox,
        "info_dir_label": info_dir_label,
        "current_dir_label": current_dir_label,
        "change_dir_button": change_dir_button,
        "apply_button": apply_button,
    }


def grid_download_frame_widgets(df_widgets: dict) -> None:
    df_widgets["tracks_info_label"].grid(row=0, column=0, padx=10, pady=5, sticky="ew")
    df_widgets["spinbox"].grid(row=0, column=1, pady=5, padx=10, sticky="ew")
    for index, widget in enumerate(list(df_widgets.values())[2:], start=1):
        widget.grid(row=index, column=0, padx=10, pady=2, sticky="nwse", columnspan=2)


def configure_download_frame_widgets(df_widgets: dict, thread: Thread, **spinbox_kwargs) -> None:

    configure_dir_label(dir_label=df_widgets["current_dir_label"])
    df_widgets["change_dir_button"].configure(
        command=lambda: open_change_dir_menu(dir_label=df_widgets["current_dir_label"])
    )
    df_widgets["apply_button"].configure(command=lambda: run_thread(thread))
    df_widgets["spinbox"].configure(**spinbox_kwargs)


def draw_download_frame(parent_frame: ctk.CTkFrame, info_label: WiffyTextLabel, **spinbox_kwargs) -> None:
    download_frame = ctk.CTkFrame(parent_frame, corner_radius=5)
    download_frame_widgets = create_download_frame_widgets(download_frame)

    download_tracks_thread = Thread(
        target=start_tracks_downloading,
        args=(
            info_label,
            parent_frame,
            download_frame,
            download_frame_widgets["spinbox"],
        ),
    )
    configure_download_frame_widgets(
        df_widgets=download_frame_widgets,
        thread=download_tracks_thread,
        to=spinbox_kwargs["tracks_count"],
        width=150,
        default_value=spinbox_kwargs["default_tracks_count"],
        max_=spinbox_kwargs["tracks_count"],
    )

    download_frame.grid(row=2, column=0, padx=10, pady=5, columnspan=2)
    grid_download_frame_widgets(download_frame_widgets)
