from threading import Thread

import customtkinter as ctk

from utils.paths import get_default_download_path, get_download_path
from wiffy_gui.config import app_settings
from wiffy_gui.items.custom import Spinbox
from wiffy_gui.items.labels import WiffyTextLabel
from wiffy_gui.layout.download.dir_menu import configure_dir_label, open_change_dir_menu


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
    df_widgets["apply_button"].configure(command=thread.start)
    df_widgets["spinbox"].configure(**spinbox_kwargs)
