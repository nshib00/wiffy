from gui import start_app
from pathlib import Path


def create_files_if_not_exist() -> None:
    Path('.env').touch()
    Path('songs_data.txt').touch()


if __name__ == "__main__":
    create_files_if_not_exist()
    start_app()
