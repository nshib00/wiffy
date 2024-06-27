import customtkinter as ctk

from wiffy_gui.config import app_settings


class LoginEntry(ctk.CTkEntry):
    def __init__(self, frame: ctk.CTkEntry, placeholder_text: str, **kwargs):
        super().__init__(
            master=frame,
            width=300,
            height=20,
            placeholder_text=placeholder_text,
            font=app_settings.base_font_small,
            **kwargs
        )
