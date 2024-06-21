import customtkinter as ctk

from wiffy_gui.app import App
from wiffy_gui.items.buttons import MainMenuButton
from wiffy_gui.config import app_settings


def create_content_frame(app: App) -> ctk.CTkFrame:
    content_frame = ctk.CTkFrame(app, width=400, height=220, corner_radius=0)
    content_frame.grid(row=2, column=0, sticky="nesw")
    return content_frame


def create_frames(app: App) -> tuple[ctk.CTkFrame, ctk.CTkFrame, ctk.CTkFrame]:
    top_frame = ctk.CTkFrame(app, width=400, height=120, corner_radius=0)
    info_text_frame = ctk.CTkFrame(app, width=400, height=60, corner_radius=0)
    content_frame = create_content_frame(app)

    top_frame.grid(row=0, column=0, sticky="nesw")
    info_text_frame.grid(row=1, column=0, sticky="nesw")
    app.grid_rowconfigure(2, weight=1)
    app.grid_rowconfigure((0, 1), weight=0)
    content_frame.grid_rowconfigure((0, 1), weight=1)
    content_frame.grid_rowconfigure(2, weight=0)

    return top_frame, info_text_frame, content_frame


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



