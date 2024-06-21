import customtkinter as ctk

from wiffy_gui.app import App


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

