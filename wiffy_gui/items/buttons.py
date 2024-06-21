from typing import Any, Callable
import customtkinter as ctk

from wiffy_gui.config import app_settings


class MainMenuButton(ctk.CTkButton):
    def __init__(
            self,
            master: Any,
            width: int = 140,
            height: int = 28,
            font=app_settings.base_font,
            text: str = "",
            command: Callable | None = None,
            **kwargs
    ):
        super().__init__(master=master, width=width, height=height, font=font, text=text, command=command, **kwargs)

    def place(self, rely, relx=0.5, anchor='center', relwidth=0.75, relheight=0.2):
        super().place(rely=rely, relx=relx, anchor=anchor, relwidth=relwidth, relheight=relheight)


class BackButton(ctk.CTkButton):
    base_width: int = app_settings.width - 40
    base_height = 40
    base_padx = 20
    base_pady = 20
    base_text = 'Back'
    base_sticky = 'nsew'

    def __init__(self, master, width: int = base_width, height: int = base_height, command: Callable | None = None,
                                                                text: str = base_text, font=app_settings.base_font, **kwargs):
        super().__init__(master=master, width=width, height=height, text=text, font=font, command=command, **kwargs)

    def grid(self, row: int = 0, column: int = 0, padx: int = base_padx, pady: int = base_pady, 
                                                            rowspan: int = 1, columnspan: int = 1, **kwargs) -> None:
        super().grid(
            row=row,
            column=column,
            padx=padx,
            pady=pady,
            sticky=self.base_sticky,
            rowspan=rowspan,
            columnspan=columnspan,
            **kwargs
        )


class SmallBackButton(BackButton):
    base_width = 30
    base_height = 80
    base_padx = 10
    base_pady = 5

