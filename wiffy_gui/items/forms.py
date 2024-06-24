import customtkinter as ctk

from wiffy_gui.items.labels import WiffyTextLabel
from wiffy_gui.config import app_settings


class LoginEntry(ctk.CTkEntry):
    def __init__(self, frame: ctk.CTkEntry, placeholder_text: str, **kwargs):
        super().__init__(master=frame, width=300, height=20, placeholder_text=placeholder_text,
                                                                                    font=app_settings.base_font_small, **kwargs)
        



# def draw_login_forms(frame: ctk.CTkFrame, info_label: WiffyTextLabel, login_button: ctk.CTkButton) -> None:
#     try:
#         info_label.clear()
#         login_button.destroy()
#         login_form = LoginEntry(frame, placeholder_text="VK phone number or email")
#         pwd_form = LoginEntry(frame, placeholder_text="VK password", show="·")
#         forms = {"login": login_form, "pwd": pwd_form}
#         save_button = ctk.CTkButton(
#             frame,
#             text="Save and continue",
#             font=app_settings.base_font,
#             height=45,
#             command=lambda: draw_main_ui(info_label=info_label, forms=forms),
#         )
#         login_form.grid(row=0, column=0, columnspan=2, padx=45, pady=10, sticky="nesw")
#         pwd_form.grid(row=1, column=0, columnspan=2, padx=45, pady=10, sticky="nesw")
#         save_button.grid(row=2, column=0, columnspan=2, padx=45, pady=40, sticky="nesw")
#     except Exception as e:
#         info_label.configure(text=e.args[0], text_color="red")