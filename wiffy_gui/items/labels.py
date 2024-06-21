import customtkinter as ctk


def clear_info_label_if_not_empty(info_label: ctk.CTkLabel) -> None:
    if info_label._text:
        info_label.configure(text="", text_color="#c0c0c0")
        