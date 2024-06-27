import customtkinter as ctk

from utils.logger import get_logger
from wiffy_gui.config import app_settings
from wiffy_gui.items.buttons import MainMenuButton

logger = get_logger(__name__)


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
