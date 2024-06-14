import base64
import os
import re

from selenium.common import SessionNotCreatedException

from parser import download_song, get_saved_songs_info, make_download_path, make_songs_data_dict, parse
from threading import Thread
from typing import Callable

import customtkinter as ctk
import requests
from customtkinter import filedialog
from dotenv import find_dotenv, load_dotenv

import utils
import widgets
from exceptions import TracksNotFoundError


logger = utils.get_logger("gui.log")


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

load_dotenv(find_dotenv())


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Wiffy")
        self.geometry("400x400")
        self.iconbitmap("images/icon-16.ico")
        self.resizable(False, False)


def create_content_frame(app: App) -> ctk.CTkFrame:
    content_frame = ctk.CTkFrame(app, width=400, height=220, corner_radius=0)
    content_frame.grid(row=2, column=0, sticky="nesw")
    return content_frame


def clear_info_label_if_not_empty(info_label: ctk.CTkLabel) -> None:
    if info_label._text:
        info_label.configure(text="", text_color="#c0c0c0")


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


def draw_wiffy_label(frame: ctk.CTkFrame) -> None:
    wiffy_label = ctk.CTkLabel(frame, text="Wiffy", font=("Arial", 60), text_color="#fc6514")
    wiffy_label.place(relx=0.5, rely=0.5, anchor="center")
    frame.grid(row=0, column=0, sticky="nesw")


def draw_login_button(frame: ctk.CTkFrame, info_label: ctk.CTkLabel, app: App, clear_frame=False) -> None:
    clear_info_label_if_not_empty(info_label)
    if clear_frame:
        frame.destroy()
        frame = create_content_frame(app)
    login_button = ctk.CTkButton(
        frame,
        text="Sign in",
        font=("Arial", 20),
        command=lambda: draw_login_forms(frame=frame, info_label=info_label, app=app, login_button=login_button),
    )
    login_button.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.7, relheight=0.2)


def draw_login_forms(frame: ctk.CTkFrame, info_label: ctk.CTkLabel, app: App, login_button: ctk.CTkButton) -> None:
    try:
        clear_info_label_if_not_empty(info_label)
        login_button.destroy()
        login_form = ctk.CTkEntry(
            frame,
            width=300,
            height=20,
            font=("Arial", 16),
            placeholder_text="VK phone number or email",
        )
        pwd_form = ctk.CTkEntry(
            frame,
            width=300,
            height=20,
            font=("Arial", 16),
            show="·",
            placeholder_text="VK password",
        )
        forms = {"login": login_form, "pwd": pwd_form}
        save_button = ctk.CTkButton(
            frame,
            text="Save and continue",
            font=("Arial", 20),
            height=45,
            command=lambda: draw_main_ui(frame=frame, app=app, info_label=info_label, forms=forms),
        )
        login_form.grid(row=0, column=0, columnspan=2, padx=45, pady=10, sticky="nesw")
        pwd_form.grid(row=1, column=0, columnspan=2, padx=45, pady=10, sticky="nesw")
        save_button.grid(row=2, column=0, columnspan=2, padx=45, pady=40, sticky="nesw")
    except Exception as e:
        info_label.configure(text=e.args[0], text_color="red")


def draw_relogin_button(
    app: App,
    top_frame: ctk.CTkFrame,
    content_frame: ctk.CTkFrame,
    info_label: ctk.CTkLabel,
) -> None:
    clear_info_label_if_not_empty(info_label)
    relogin_button = ctk.CTkButton(
        top_frame,
        text="⭮",
        font=("Arial", 35),
        command=lambda: draw_login_button(frame=content_frame, info_label=info_label, app=app, clear_frame=True),
    )
    relogin_button.place(relx=0.9, rely=0.25, anchor="center", relwidth=0.1, relheight=0.32)


def draw_back_button(
    frame: ctk.CTkFrame,
    width: int = 360,
    height: int = 40,
    row: int = 0,
    column: int = 0,
    command: Callable = None,
    padx: int = 20,
    pady: int = 20,
    rowspan: int = 1,
    columnspan: int = 1,
    **kwargs,
) -> None:
    back_button = ctk.CTkButton(
        frame,
        text="Back",
        width=width,
        height=height,
        font=("Arial", 20),
        command=command,
        **kwargs,
    )
    back_button.grid(
        row=row,
        column=column,
        padx=padx,
        pady=pady,
        sticky="nsew",
        rowspan=rowspan,
        columnspan=columnspan,
    )


def open_show_songs_menu(app: App, info_label: ctk.CTkLabel, content_frame: ctk.CTkFrame) -> None:
    clear_info_label_if_not_empty(info_label)
    content_frame.destroy()
    content_frame = ctk.CTkFrame(app, corner_radius=0)
    songs_frame = ctk.CTkScrollableFrame(content_frame, width=360, height=130, label_anchor="w")
    saved_songs_str, saved_songs_count = get_saved_songs_info()
    content_frame.grid(row=2, column=0)
    songs_label = ctk.CTkLabel(songs_frame, text=saved_songs_str)
    if saved_songs_count:
        songs_frame.grid(row=0, column=0, padx=10, pady=5)
        songs_label.pack()
        info_label.configure(text=f"Songs found: {saved_songs_count}.", text_color="green")
        draw_back_button(
            width=30,
            height=80,
            frame=content_frame,
            row=1,
            column=0,
            padx=10,
            pady=5,
            command=lambda: draw_main_ui(info_label=info_label, app=app, clear_frame=True, frame=content_frame),
        )
        content_frame.grid_rowconfigure(0, weight=2)
        content_frame.grid_rowconfigure(1, weight=1)
    else:
        info_label.configure(
            text="There are no saved tracks. Before downloading,\nclick on the “find tracks” "
            "button so that the program saves\ninformation about tracks from your VK page.",
            text_color="#ffaa00",
        )
    draw_back_button(
        frame=content_frame,
        row=1,
        column=0,
        padx=10,
        pady=5,
        command=lambda: draw_main_ui(info_label=info_label, app=app, clear_frame=True, frame=content_frame),
    )


def start_tracks_parsing(info_label: ctk.CTkLabel) -> None:
    clear_info_label_if_not_empty(info_label)
    info_label.configure(text="Getting data about tracks from VK page...", text_color="#c0c0c0")
    try:
        requests.get("https://kissvk.com")
        parse()
    except requests.ConnectionError as e:
        info_label.configure(
            text="No internet connection. To find tracks from VK,\nyou need to connect to internet and try again.",
            text_color="red",
        )
        logger.error(f"{e.__class__.__name__}: {e}")
    except SessionNotCreatedException as e:
        current_driver_version = re.search(r'only supports Chrome version [\d.]+', str(e)).group(0).split(' ')[-1]
        browser_version = re.search(r'Current browser version is [\d.]+', str(e)).group(0).split(' ')[-1]
        utils.save_driver_version_info(version_info=browser_version)
        info_label.configure(
            text=f"Driver session error. Current driver version: {current_driver_version}.\nDriver needs to be updated to version {browser_version} to work correctly.",
            text_color="red",
        )
        logger.error(f"{e.__class__.__name__}: {e}")
    # except WebDriverException as e:
    #     info_label.configure(
    #         text="Parser exception occured.\nProbably, the page didn't load "
    #         "in time because of slow\ninternet connection.",
    #         text_color="red",
    #     )
    #     logger.error(f"{e.__class__.__name__}: {e}")
    except Exception as e:
        info_label.configure(text=f"Error occured: {e.__class__.__name__}.", text_color="red")
        logger.error(f"{e.__class__.__name__}: {e}")
    else:
        info_label.configure(
            text='Tracks from VK found succesfully.\nYou can click the "Show found tracks" button to check it.',
            text_color="green",
        )


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
            dir_label.configure(text=utils.get_default_download_path())


def create_and_get_download_frame_widgets(download_frame: ctk.CTkFrame, download_path: str) -> dict:
    tracks_info_label = ctk.CTkLabel(download_frame, text="Tracks to download:")
    spinbox = widgets.Spinbox(download_frame, width=120)
    info_dir_label = ctk.CTkLabel(download_frame, text="Current download folder:")
    current_dir_label = ctk.CTkLabel(download_frame, text=download_path)
    change_dir_button = ctk.CTkButton(download_frame, text="Change", font=("Arial", 20))
    apply_button = ctk.CTkButton(download_frame, text="Apply and download", font=("Arial", 20))
    return {
        "tracks_info_label": tracks_info_label,
        "spinbox": spinbox,
        "info_dir_label": info_dir_label,
        "current_dir_label": current_dir_label,
        "change_dir_button": change_dir_button,
        "apply_button": apply_button,
    }


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


def draw_download_frame(parent_frame: ctk.CTkFrame, info_label: ctk.CTkLabel, **spinbox_kwargs) -> None:
    download_frame = ctk.CTkFrame(parent_frame, corner_radius=5)

    download_path = utils.get_download_path() or utils.get_default_download_path()
    download_frame_widgets = create_and_get_download_frame_widgets(download_frame, download_path)

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


def open_download_menu(app: App, content_frame: ctk.CTkFrame, info_label: ctk.CTkLabel) -> None:
    clear_info_label_if_not_empty(info_label)
    # content_frame.destroy()
    content_frame = create_content_frame(app)

    tracks_count = utils.count_saved_tracks()
    default_tracks_count = 50 if tracks_count >= 50 else tracks_count

    draw_download_frame(
        parent_frame=content_frame,
        info_label=info_label,
        tracks_count=tracks_count,
        default_tracks_count=default_tracks_count,
    )

    draw_back_button(
        content_frame,
        row=3,
        width=380,
        height=30,
        padx=10,
        pady=5,
        columnspan=2,
        command=lambda: draw_main_ui(info_label=info_label, app=app, clear_frame=True, frame=content_frame),
    )


def open_change_dir_menu(dir_label: ctk.CTkLabel) -> None:
    new_download_path = filedialog.askdirectory()
    utils.change_download_path(new_download_path)
    configure_dir_label(dir_label, new_path=new_download_path)


def create_progressbar_elements(pb_frame: ctk.CTkFrame, songs_count: int) -> tuple[ctk.CTkProgressBar, ctk.CTkLabel]:
    progressbar = ctk.CTkProgressBar(pb_frame, width=320, corner_radius=5)
    pb_label = ctk.CTkLabel(pb_frame, text=f"0/{songs_count}")
    return progressbar, pb_label


def grid_progressbar_elements(pb_frame: ctk.CTkFrame, pb: ctk.CTkProgressBar, pb_label: ctk.CTkLabel) -> None:
    pb_frame.grid(row=0, column=0, padx=10, pady=5, columnspan=2)  # grids on content frame

    # grids on progressbar frame
    pb.grid(row=0, column=0, padx=5, pady=5)
    pb_label.grid(row=0, column=1, padx=5, pady=5)


def download_songs_with_progressbar(
    pb: ctk.CTkProgressBar, pb_label: ctk.CTkLabel, songs_count: int | None = None
) -> None:
    songs_data = make_songs_data_dict(count=songs_count)
    for index, song in enumerate(songs_data, start=1):
        download_path = make_download_path()
        download_song(song, download_path)
        pb.set(value=index / songs_count)
        pb_label.configure(text=f"{index}/{songs_count}")


def start_tracks_downloading(
    info_label: ctk.CTkLabel,
    content_frame: ctk.CTkFrame,
    download_frame: ctk.CTkFrame,
    spinbox: widgets.Spinbox,
) -> None:
    info_label.configure(text="Downloading tracks...", text_color="#c0c0c0")
    choosed_tracks_count = spinbox.get()
    saved_tracks_count = utils.count_saved_tracks()
    if choosed_tracks_count is None:
        choosed_tracks_count = saved_tracks_count
    download_frame.grid_forget()
    progressbar_frame = ctk.CTkFrame(content_frame, width=360, height=50)
    progressbar, pb_label = create_progressbar_elements(progressbar_frame, songs_count=int(choosed_tracks_count))
    grid_progressbar_elements(pb_frame=progressbar_frame, pb=progressbar, pb_label=pb_label)
    progressbar.set(0)
    try:
        if int(choosed_tracks_count) > saved_tracks_count:
            raise ValueError(f"Incorrect value. Tracks count should be between 1 and {saved_tracks_count}.")
        if choosed_tracks_count is None:
            download_songs_with_progressbar(pb=progressbar, pb_label=pb_label)
        else:
            download_songs_with_progressbar(pb=progressbar, pb_label=pb_label, songs_count=int(choosed_tracks_count))
    except TracksNotFoundError as e:
        info_label.configure(
            text="There are no saved tracks. Before downloading,\nclick on the “Find tracks from VK”"
            "button so that the program saves\ninformation about tracks from your VK page.",
            text_color="red",
        )
        logger.error(f"{e.__class__.__name__}: {e}")
    except ValueError as e:
        info_label.configure(text=e.args[0], text_color="red")
        logger.error(f"{e.__class__.__name__}: {e}")
    except Exception as e:
        info_label.configure(text=f"Error occured: {e.__class__.__name__}.", text_color="red")
        logger.error(f"{e.__class__.__name__}: {e}")
    else:
        info_label.configure(text="Tracks downloaded successfully.", text_color="green")


def draw_main_ui(
    frame: ctk.CTkFrame,
    app: App,
    info_label: ctk.CTkLabel,
    forms: dict | None = None,
    clear_frame: bool = False,
) -> None:
    clear_info_label_if_not_empty(info_label)
    if clear_frame:
        frame.destroy()
        frame = create_content_frame(app)
    try:
        if forms is not None:
            if forms.get("login") is not None and forms.get("pwd") is not None:
                login = forms["login"].get()
                utils.set_pwd(base64.b64encode(forms.get("pwd").get().encode("utf-8")))
                pwd = utils.get_pwd()
                email_regex = utils.get_email_regex()
                phone_number_regex = utils.get_phone_number_regex()

                if not login or not pwd:
                    raise ValueError("Login and/or password are not specified. Please, try again.")
                if utils.string_is_email(string=login):
                    if not email_regex.match(login):
                        raise ValueError("Email is incorrect. Please, try again.")
                else:
                    if not phone_number_regex.match(login):
                        raise ValueError("Phone number is incorrect. Please, try again.")
                    if len(forms["pwd"].get()) < 8:
                        raise ValueError("VK password cannot contain less than 8 characters.\nPlease, try again.")
                utils.save_vk_login(login)
                frame.destroy()
        frame = create_content_frame(app)
        tracks_parsing_thread = Thread(target=start_tracks_parsing, args=(info_label,))
        find_tracks_button = ctk.CTkButton(
            frame,
            text="Find tracks from VK",
            font=("Arial", 20),
            command=tracks_parsing_thread.start,
        )
        find_tracks_button.place(relx=0.5, rely=0.2, anchor="center", relwidth=0.75, relheight=0.2)
        show_tracks_button = ctk.CTkButton(
            frame,
            text="Show found tracks",
            font=("Arial", 20),
            command=lambda: open_show_songs_menu(app=app, content_frame=frame, info_label=info_label),
        )
        show_tracks_button.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.75, relheight=0.2)
        download_tracks_button = ctk.CTkButton(
            frame,
            text="Download found tracks",
            font=("Arial", 20),
            command=lambda: open_download_menu(app=app, content_frame=frame, info_label=info_label),
        )
        download_tracks_button.place(relx=0.5, rely=0.8, anchor="center", relwidth=0.75, relheight=0.2)
    except ValueError as e:
        info_label.configure(text=e.args[0], text_color="red")
        logger.error(f"{e.__class__.__name__}: {e}")


def draw_ui(app: App) -> None:
    top_frame, info_text_frame, content_frame = create_frames(app)
    info_label = ctk.CTkLabel(info_text_frame, text="")
    info_label.place(relx=0.5, rely=0.5, anchor="center")
    draw_wiffy_label(frame=top_frame)
    draw_relogin_button(app=app, top_frame=top_frame, content_frame=content_frame, info_label=info_label)
    if os.getenv("VK_LOGIN") is None or utils.get_pwd() is None:
        draw_login_button(frame=content_frame, info_label=info_label, app=app)
    else:
        draw_main_ui(frame=content_frame, info_label=info_label, app=app)


def start_app() -> None:
    app = App()
    draw_ui(app)
    app.mainloop()
