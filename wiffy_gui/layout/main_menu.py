import customtkinter as ctk

from wiffy_gui import text
from wiffy_gui.config import app_settings
from wiffy_gui.items.buttons import MainMenuButton


def place_main_menu_buttons(buttons: tuple[ctk.CTkButton]) -> None:
    rely = 0.2
    for button in buttons:
        button.place(relx=0.5, rely=rely, anchor="center", relwidth=0.75, relheight=0.2)
        rely += 0.3


def create_main_menu_buttons(content_frame: ctk.CTkFrame) -> tuple[ctk.CTkButton]:
    find_tracks_button = MainMenuButton(
        content_frame,
        text=text.FIND_TRACKS_BUTTON_LABEL,
        font=app_settings.base_font,
    )
    show_tracks_button = MainMenuButton(
        content_frame,
        text=text.SHOW_TRACKS_BUTTON_LABEL,
        font=app_settings.base_font,
    )
    download_tracks_button = MainMenuButton(
        content_frame,
        text=text.DOWNLOAD_TRACKS_BUTTON_LABEL,
        font=app_settings.base_font,
    )
    buttons = find_tracks_button, show_tracks_button, download_tracks_button
    place_main_menu_buttons(buttons)
    return buttons
