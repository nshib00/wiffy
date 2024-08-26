from typing import Callable

import customtkinter as ctk

from wiffy_gui.text import SPINBOX_ALL_BUTTON_TEXT


class Spinbox(ctk.CTkFrame):
    def __init__(
        self,
        master,
        width: int = 100,
        height: int = 30,
        step: int = 1,
        command: Callable | None = None,
        from_: int = 0,
        to: int = 100,
        default_value: int = 0,
        max_: int | None = None,
        *args,
        **kwargs
    ):
        super().__init__(*args, master=master, width=width, height=height, **kwargs)
        self.step = step
        self.command = command
        self.from_ = from_
        self.to = to
        self.default_value = default_value
        self.value = self.default_value
        self.max_ = max_

        self.minus_button = ctk.CTkButton(
            self,
            text="-",
            width=int(0.3 * width),
            height=height - 5,
            command=self.subtract_value,
        )
        self.value_entry = ctk.CTkEntry(self, width=int(0.5 * width), height=height - 5)
        self.value_entry.insert(0, self.value)
        self.plus_button = ctk.CTkButton(
            self,
            text="+",
            width=int(0.3 * width),
            height=height - 5,
            command=self.add_value,
        )
        self.all_tracks_button = ctk.CTkButton(
            self,
            text=SPINBOX_ALL_BUTTON_TEXT,
            width=int(0.3 * width),
            height=height - 5,
            command=self.set_max_value,
        )
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((0, 2, 3), weight=0)

        self.minus_button.grid(row=0, column=0, padx=5)
        self.value_entry.grid(row=0, column=1, padx=5)
        self.plus_button.grid(row=0, column=2, padx=5)
        self.all_tracks_button.grid(row=0, column=3, padx=5)

    def subtract_value(self) -> None:
        self.value -= 1
        self.value_entry.delete(0, "end")
        self.value_entry.insert(0, self.value)

    def add_value(self) -> None:
        self.value += 1
        self.value_entry.delete(0, "end")
        self.value_entry.insert(0, self.value)

    def get(self) -> int | None:
        try:
            return self.value_entry.get()
        except ValueError:
            return None

    def set_max_value(self) -> None:
        self.value_entry.delete(0, "end")
        self.value_entry.insert(0, self.max_)

    def configure(
        self,
        from_: int | None = None,
        to: int | None = None,
        default_value: int | None = None,
        max_: int | None = None,
        require_redraw=False,
        **kwargs
    ):
        arg_names = ("from_", "to", "default_value", "max_")
        arg_values = (from_, to, default_value, max_)
        for argname, argvalue in zip(arg_names, arg_values):
            if argvalue is not None:
                setattr(self, argname, argvalue)
        super().configure(require_redraw, **kwargs)
