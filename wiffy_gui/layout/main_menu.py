import base64
from threading import Thread
import customtkinter as ctk

from utils.user_data import save_vk_login, set_pwd
from utils.validation import validate_user_data
from wiffy_gui.items.buttons import MainMenuButton
from wiffy_gui.config import app_settings
from wiffy_gui.items.frames import create_content_frame, create_frames
from wiffy_gui.items.labels import WiffyTextLabel, draw_app_header
from utils.logger import get_logger
from wiffy_gui.parsing import start_tracks_parsing


logger = get_logger(__file__)


def place_main_menu_buttons(buttons: tuple[ctk.CTkButton]) -> None:
    rely = 0.2
    for button in buttons:
        button.place(relx=0.5, rely=rely, anchor="center", relwidth=0.75, relheight=0.2)
        rely += 0.3


def create_main_menu_buttons(content_frame: ctk.CTkFrame) -> tuple[ctk.CTkButton]:
    find_tracks_button = MainMenuButton(
    content_frame,
        text="Find tracks from VK",
        font=app_settings.base_font,
    )
    show_tracks_button = MainMenuButton(
        content_frame,
        text="Show found tracks",
        font=app_settings.base_font,
        
    )
    download_tracks_button = MainMenuButton(
        content_frame,
        text="Download found tracks",
        font=app_settings.base_font,
    )
    buttons = find_tracks_button, show_tracks_button, download_tracks_button
    place_main_menu_buttons(buttons)
    return buttons


def configure_main_menu_buttons(buttons: tuple[MainMenuButton], info_label: WiffyTextLabel,
                                                                                    content_frame: ctk.CTkFrame) -> None:
    tracks_parsing_thread = Thread(target=start_tracks_parsing, args=(info_label,))
    find_tracks_button, show_tracks_button, download_tracks_button = buttons

    find_tracks_button.configure(command=tracks_parsing_thread.start)
    # show_tracks_button.configure(
    #     command=lambda: open_show_songs_menu(content_frame=content_frame, info_label=info_label)
    # )
    # download_tracks_button.configure(
    #     command=lambda: open_download_menu(content_frame=content_frame, info_label=info_label)
    # )


def draw_main_menu(
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

