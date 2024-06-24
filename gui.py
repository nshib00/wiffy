import os

from utils.user_data import get_pwd
from utils.counters import get_tracks_count

from wiffy_gui.app import app
from wiffy_gui.items.buttons import BackButton
from wiffy_gui.items.frames import create_content_frame, create_frames
from wiffy_gui.items.labels import WiffyTextLabel, draw_app_header
from wiffy_gui.layout.download_menu import draw_download_frame
from wiffy_gui.layout.login import draw_login_button, draw_relogin_button
from wiffy_gui.layout.main_menu import draw_main_menu
from wiffy_gui.layout.show_songs_menu import configure_ssm_grid
from wiffy_parser.songs_data import get_saved_songs_info
from typing import Callable

import customtkinter as ctk
from dotenv import find_dotenv, load_dotenv

from utils.logger import get_logger


logger = get_logger(__file__)


load_dotenv(find_dotenv())


def draw_back_button(
    frame: ctk.CTkFrame,
    width: int = 360,
    height: int = 40,
    row: int = 0,
    column: int = 0,
    command: Callable = None,
    padx: int = 20,
    pady: int = 20,
    rowspan: int = 1,
    columnspan: int = 1,
    **kwargs,
) -> None:
    back_button = BackButton(
        frame,
        width=width,
        height=height,
        command=command,
        **kwargs,
    )
    back_button.grid(
        row=row,
        column=column,
        padx=padx,
        pady=pady,
        rowspan=rowspan,
        columnspan=columnspan,
    )


def open_show_songs_menu(info_label: WiffyTextLabel, content_frame: ctk.CTkFrame) -> None:
    info_label.clear()
    content_frame.destroy()
    content_frame = ctk.CTkFrame(app, corner_radius=0)
    songs_frame = ctk.CTkScrollableFrame(content_frame, width=360, height=130, label_anchor="w")
    saved_songs_str, saved_songs_count = get_saved_songs_info()
    content_frame.grid(row=2, column=0)
    songs_label = WiffyTextLabel(songs_frame, text=saved_songs_str)
    if saved_songs_count:
        songs_frame.grid(row=0, column=0, padx=10, pady=5)
        songs_label.pack()
        info_label.configure(text=f"Songs found: {saved_songs_count}.", text_color="green")
        draw_back_button(
            width=30,
            height=80,
            frame=content_frame,
            row=1,
            column=0,
            padx=10,
            pady=5,
            command=lambda: draw_main_menu(app=app, clear_frame=True),
        )
        configure_ssm_grid(content_frame)
    else:
        info_label.configure(
            text="There are no saved tracks. Before downloading,\nclick on the “find tracks” "
            "button so that the program saves\ninformation about tracks from your VK page.",
            text_color="#ffaa00",
        )
    draw_back_button(
        frame=content_frame,
        row=1,
        column=0,
        padx=10,
        pady=5,
        command=lambda: draw_main_menu(clear_frame=True),
    )


def open_download_menu(content_frame: ctk.CTkFrame, info_label: WiffyTextLabel) -> None:
    info_label.clear()
    content_frame = create_content_frame()

    draw_download_frame(
        parent_frame=content_frame,
        info_label=info_label,
        tracks_count=get_tracks_count(),
        default_tracks_count=get_tracks_count(get_default=True),
    )

    draw_back_button(
        content_frame,
        row=3,
        width=380,
        height=30,
        padx=10,
        pady=5,
        columnspan=2,
        command=lambda: draw_main_menu(clear_frame=True),
    )


def draw_ui() -> None:
    top_frame, info_text_frame, content_frame = create_frames()
    info_label = WiffyTextLabel(info_text_frame)
    info_label.place(relx=0.5, rely=0.5, anchor="center")
    draw_app_header(frame=top_frame)
    draw_relogin_button(top_frame=top_frame, content_frame=content_frame, info_label=info_label)
    if os.getenv("VK_LOGIN") is None or get_pwd() is None:
        draw_login_button(frame=content_frame, info_label=info_label)
    else:
        draw_main_menu()


def start_app() -> None:
    draw_ui()
    app.mainloop()
