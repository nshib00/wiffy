from os import getenv
from pathlib import Path

from dotenv import find_dotenv, load_dotenv, set_key

envfile = find_dotenv()
load_dotenv(envfile)


def get_default_download_path() -> str:
    default_download_path_obj = Path("~/Downloads/wiffy")
    return str(default_download_path_obj.expanduser())


def change_download_path(new_path: str) -> None:
    if Path(new_path).is_dir():
        set_key(envfile, "DOWNLOAD_PATH", new_path)
    else:
        set_key(envfile, "DOWNLOAD_PATH", get_default_download_path())


def get_download_path() -> str:
    return getenv("DOWNLOAD_PATH")


def make_download_path() -> Path:
    if getenv("DOWNLOAD_PATH") is not None:
        download_path = Path(getenv("DOWNLOAD_PATH"))
    else:
        download_path = Path("~/Downloads/wiffy")
    if not download_path.is_dir():
        download_path.mkdir(exist_ok=True, parents=True)
    return download_path
