from threading import Thread

import customtkinter as ctk

from utils.threads import run_thread
from wiffy_gui.download import start_tracks_downloading
from wiffy_gui.items.labels import WiffyTextLabel
from wiffy_gui.layout.dir_menu import configure_dir_label, open_change_dir_menu
from wiffy_gui.layout.download.widgets import create_download_frame_widgets


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
        daemon=True,
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
