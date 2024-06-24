import customtkinter as ctk

from utils.paths import change_download_path, get_default_download_path


def configure_dir_label(dir_label: ctk.CTkLabel, new_path: str | None = None) -> None:
    if new_path is None:
        label_text = dir_label.cget("text")
        if len(label_text) > 50:
            dir_label.configure(text=label_text[:50] + "...")
    else:
        if new_path:
            if len(new_path) <= 50:
                dir_label.configure(text=new_path)
            else:
                dir_label.configure(text=new_path[:50] + "...")
        else:
            dir_label.configure(text=get_default_download_path())


def open_change_dir_menu(dir_label: ctk.CTkLabel) -> None:
    new_download_path = ctk.filedialog.askdirectory()
    change_download_path(new_download_path)
    configure_dir_label(dir_label, new_path=new_download_path)