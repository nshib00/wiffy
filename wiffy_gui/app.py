import customtkinter as ctk


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Wiffy")
        self.geometry("400x400")
        self.iconbitmap("images/icon-16.ico")
        self.resizable(False, False)
    