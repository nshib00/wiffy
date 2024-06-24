import base64
import os

from utils.user_data import get_pwd, set_pwd, save_vk_login
from utils.counters import get_tracks_count
from utils.validation import validate_user_data
from wiffy_gui.app import app
from wiffy_gui.items.buttons import BackButton, MainMenuButton
from wiffy_gui.items.labels import WiffyTextLabel, draw_app_header
from wiffy_gui.layout.download_menu import draw_download_frame
from wiffy_gui.layout.main_menu import create_main_menu_buttons, create_content_frame, create_frames
from wiffy_gui.layout.show_songs_menu import configure_ssm_grid
from wiffy_gui.parsing import start_tracks_parsing
from wiffy_parser.songs_data import get_saved_songs_info
from wiffy_gui.config import app_settings
from threading import Thread
from typing import Callable

import customtkinter as ctk
from dotenv import find_dotenv, load_dotenv

from utils.logger import get_logger


logger = get_logger(__file__)


load_dotenv(find_dotenv())


def configure_main_menu_buttons(buttons: tuple[MainMenuButton], info_label: WiffyTextLabel,
                                                                                    content_frame: ctk.CTkFrame) -> None:
    tracks_parsing_thread = Thread(target=start_tracks_parsing, args=(info_label,))
    find_tracks_button, show_tracks_button, download_tracks_button = buttons

    find_tracks_button.configure(command=tracks_parsing_thread.start)
    show_tracks_button.configure(
        command=lambda: open_show_songs_menu(content_frame=content_frame, info_label=info_label)
    )
    download_tracks_button.configure(
        command=lambda: open_download_menu(content_frame=content_frame, info_label=info_label)
    )


def draw_login_button(frame: ctk.CTkFrame, info_label: WiffyTextLabel, clear_frame=False) -> None:
    info_label.clear()
    if clear_frame:
        frame.destroy()
        frame = create_content_frame()
    login_button = ctk.CTkButton(
        frame,
        text="Sign in",
        font=app_settings.base_font,
        command=lambda: draw_login_forms(frame=frame, info_label=info_label, login_button=login_button),
    )
    login_button.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.7, relheight=0.2)


def draw_login_forms(frame: ctk.CTkFrame, info_label: WiffyTextLabel, login_button: ctk.CTkButton) -> None:
    try:
        info_label.clear()
        login_button.destroy()
        login_form = ctk.CTkEntry(
            frame,
            width=300,
            height=20,
            font=app_settings.base_font_small,
            placeholder_text="VK phone number or email",
        )
        pwd_form = ctk.CTkEntry(
            frame,
            width=300,
            height=20,
            font=app_settings.base_font_small,
            show="·",
            placeholder_text="VK password",
        )
        forms = {"login": login_form, "pwd": pwd_form}
        save_button = ctk.CTkButton(
            frame,
            text="Save and continue",
            font=app_settings.base_font,
            height=45,
            command=lambda: draw_main_ui(forms=forms),
        )
        login_form.grid(row=0, column=0, columnspan=2, padx=45, pady=10, sticky="nesw")
        pwd_form.grid(row=1, column=0, columnspan=2, padx=45, pady=10, sticky="nesw")
        save_button.grid(row=2, column=0, columnspan=2, padx=45, pady=40, sticky="nesw")
    except Exception as e:
        info_label.configure(text=e.args[0], text_color="red")


def draw_relogin_button(
    top_frame: ctk.CTkFrame,
    content_frame: ctk.CTkFrame,
    info_label: WiffyTextLabel,
) -> None:
    info_label.clear()
    relogin_button = ctk.CTkButton(
        top_frame,
        text="⭮",
        font=app_settings.base_font_big,
        command=lambda: draw_login_button(frame=content_frame, info_label=info_label, clear_frame=True),
    )
    relogin_button.place(relx=0.9, rely=0.25, anchor="center", relwidth=0.1, relheight=0.32)


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
            command=lambda: draw_main_ui(app=app, clear_frame=True),
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
        command=lambda: draw_main_ui(clear_frame=True),
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
        command=lambda: draw_main_ui(clear_frame=True),
    )


def draw_main_ui(
    forms: dict | None = None,
    clear_frame: bool = False,
) -> None:
    top_frame, info_text_frame, frame = create_frames()
    info_label = WiffyTextLabel(info_text_frame)
    info_label.place(relx=0.5, rely=0.5, anchor="center")
    draw_app_header(frame=top_frame)
    info_label.clear()
    if clear_frame:
        frame.destroy()
        frame = create_content_frame()
    try:
        if forms is not None:
            if forms.get("login") is not None and forms.get("pwd") is not None:
                login = forms["login"].get()
                set_pwd(base64.b64encode(forms.get("pwd").get().encode("utf-8")))
                validate_user_data(login=login)
                save_vk_login(login)
                frame.destroy()
        frame = create_content_frame()
        menu_buttons = create_main_menu_buttons(frame)
        configure_main_menu_buttons(buttons=menu_buttons, info_label=info_label, content_frame=frame)
    except FileNotFoundError as e:
        info_label.configure(text='You have no saved tracks. Try to find tracks before.', text_color="red")
        logger.error(f"{e.__class__.__name__}: {e}")
    except ValueError as e:
        info_label.configure(text=e.args[0], text_color="red")
        logger.error(f"{e.__class__.__name__}: {e}")


def draw_ui() -> None:
    top_frame, info_text_frame, content_frame = create_frames()
    info_label = WiffyTextLabel(info_text_frame)
    info_label.place(relx=0.5, rely=0.5, anchor="center")
    draw_app_header(frame=top_frame)
    draw_relogin_button(top_frame=top_frame, content_frame=content_frame, info_label=info_label)
    if os.getenv("VK_LOGIN") is None or get_pwd() is None:
        draw_login_button(frame=content_frame, info_label=info_label)
    else:
        draw_main_ui()


def start_app() -> None:
    draw_ui()
    app.mainloop()
