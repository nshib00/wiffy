from threading import Thread
from wiffy_gui.layout.dir_menu import configure_dir_label, open_change_dir_menu


def grid_download_frame_widgets(df_widgets: dict) -> None:
    df_widgets["tracks_info_label"].grid(row=0, column=0, padx=10, pady=5, sticky="ew")
    df_widgets["spinbox"].grid(row=0, column=1, pady=5, padx=10, sticky="ew")
    for index, widget in enumerate(list(df_widgets.values())[2:], start=1):
        widget.grid(row=index, column=0, padx=10, pady=2, sticky="nwse", columnspan=2)


def configure_download_frame_widgets(df_widgets: dict, thread: Thread, **spinbox_kwargs) -> None:
    
    configure_dir_label(dir_label=df_widgets["current_dir_label"])
    df_widgets["change_dir_button"].configure(
        command=lambda: open_change_dir_menu(dir_label=df_widgets["current_dir_label"])
    )
    df_widgets["apply_button"].configure(command=thread.start)
    df_widgets["spinbox"].configure(**spinbox_kwargs)