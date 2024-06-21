import customtkinter as ctk

from gui import clear_info_label_if_not_empty
from wiffy_gui.app import App
from wiffy_parser.songs_data import get_saved_songs_info


# SSM means 'show songs menu'.


def configure_ssm_grid(content_frame: ctk.CTkFrame) -> None:
    content_frame.grid_rowconfigure(0, weight=2)
    content_frame.grid_rowconfigure(1, weight=1)
    