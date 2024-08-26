import customtkinter as ctk

# ssm означает 'show songs menu'


def configure_ssm_grid(content_frame: ctk.CTkFrame) -> None:
    content_frame.grid_rowconfigure(0, weight=2)
    content_frame.grid_rowconfigure(1, weight=1)
