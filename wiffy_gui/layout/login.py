import customtkinter as ctk

from wiffy_gui.items.forms import LoginEntry
from wiffy_gui.items.labels import WiffyTextLabel
from wiffy_gui.config import app_settings
from wiffy_gui.layout.main_menu import create_content_frame, draw_main_menu


def draw_login_button(frame: ctk.CTkFrame, info_label: WiffyTextLabel, clear_frame=False) -> None:
    info_label.clear()
    if clear_frame:
        frame.destroy()
        frame = create_content_frame()
    login_button = ctk.CTkButton(
        frame,
        text="Sign in",
        font=app_settings.base_font,
        command=lambda: draw_login_forms(frame=frame, info_label=info_label, login_button=login_button),
    )
    login_button.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.7, relheight=0.2)


def draw_relogin_button(
    top_frame: ctk.CTkFrame,
    content_frame: ctk.CTkFrame,
    info_label: WiffyTextLabel,
) -> None:
    info_label.clear()
    relogin_button = ctk.CTkButton(
        top_frame,
        text="⭮",
        font=app_settings.base_font_big,
        command=lambda: draw_login_button(frame=content_frame, info_label=info_label, clear_frame=True),
    )
    relogin_button.place(relx=0.9, rely=0.25, anchor="center", relwidth=0.1, relheight=0.32)


def draw_login_forms(frame: ctk.CTkFrame, info_label: WiffyTextLabel, login_button: ctk.CTkButton) -> None:
    try:
        info_label.clear()
        login_button.destroy()
        login_form = LoginEntry(frame, placeholder_text="VK phone number or email")
        pwd_form = LoginEntry(frame, show="·", placeholder_text="VK password")
        forms = {"login": login_form, "pwd": pwd_form}
        save_button = ctk.CTkButton(
            frame,
            text="Save and continue",
            font=app_settings.base_font,
            height=45,
            command=lambda: draw_main_menu(forms=forms),
        )
        login_form.grid(row=0, column=0, columnspan=2, padx=45, pady=10, sticky="nesw")
        pwd_form.grid(row=1, column=0, columnspan=2, padx=45, pady=10, sticky="nesw")
        save_button.grid(row=2, column=0, columnspan=2, padx=45, pady=40, sticky="nesw")
    except Exception as e:
        info_label.configure(text=e.args[0], text_color="red")

