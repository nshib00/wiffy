from pathlib import Path
import os
from dotenv import load_dotenv

from wiffy_gui.core import start_app


def create_files_if_not_exist() -> None:
    Path(".env").touch()
    load_dotenv('.env')
    if os.getenv('DOWNLOAD_PATH') is None:
        user_downloads_path = Path('~').expanduser() / 'Downloads'
        os.environ['DOWNLOAD_PATH'] = str(user_downloads_path) 
    Path("songs_data.txt").touch()


if __name__ == "__main__":
    create_files_if_not_exist()
    start_app()
