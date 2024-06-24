import customtkinter as ctk
from threading import Thread

from wiffy_gui.download import start_tracks_downloading
from wiffy_gui.items.labels import WiffyTextLabel
from wiffy_gui.layout.download.widgets import configure_download_frame_widgets, create_download_frame_widgets, grid_download_frame_widgets


def draw_download_frame(parent_frame: ctk.CTkFrame, info_label: WiffyTextLabel, **spinbox_kwargs) -> None:
    download_frame = ctk.CTkFrame(parent_frame, corner_radius=5)
    download_frame_widgets = create_download_frame_widgets(download_frame)

    download_tracks_thread = Thread(
        target=start_tracks_downloading,
        args=(
            info_label,
            parent_frame,
            download_frame,
            download_frame_widgets["spinbox"],
        ),
    )
    configure_download_frame_widgets(
        df_widgets=download_frame_widgets,
        thread=download_tracks_thread,
        to=spinbox_kwargs["tracks_count"],
        width=150,
        default_value=spinbox_kwargs["default_tracks_count"],
        max_=spinbox_kwargs["tracks_count"],
    )

    download_frame.grid(row=2, column=0, padx=10, pady=5, columnspan=2)
    grid_download_frame_widgets(download_frame_widgets)
