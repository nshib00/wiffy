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


def draw_app_header(frame: ctk.CTkFrame) -> None:
    wiffy_label = WiffyTextLabel(
        frame,
        text="Wiffy",
        font=app_settings.base_font_header,
        text_color=app_settings.header_color,
    )
    wiffy_label.place_in_center()
    frame.grid(row=0, column=0, sticky="nesw")
