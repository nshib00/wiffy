import customtkinter as ctk


def create_progressbar_elements(pb_frame: ctk.CTkFrame, songs_count: int) -> tuple[ctk.CTkProgressBar, ctk.CTkLabel]:
    progressbar = ctk.CTkProgressBar(pb_frame, width=320, corner_radius=5)
    pb_label = ctk.CTkLabel(pb_frame, text=f"0/{songs_count}")
    return progressbar, pb_label


def grid_progressbar_elements(pb_frame: ctk.CTkFrame, pb: ctk.CTkProgressBar, pb_label: ctk.CTkLabel) -> None:
    pb_frame.grid(row=0, column=0, padx=10, pady=5, columnspan=2)  # grids on content frame

    # grids on progressbar frame
    pb.grid(row=0, column=0, padx=5, pady=5)
    pb_label.grid(row=0, column=1, padx=5, pady=5)
