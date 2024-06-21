import customtkinter as ctk
from wiffy_gui.config import app_settings


class WiffyTextLabel(ctk.CTkLabel):
    def __init__(self, master, text="", text_color=app_settings.text_color, **kwargs):
        super().__init__(master=master, text=text, text_color=text_color, **kwargs)

    def clear(self) -> None:
        if self._text:
            self.configure(text="", text_color=app_settings.text_color)

    def place_in_center(self) -> None:
        super().place(relx=0.5, rely=0.5, anchor="center")

