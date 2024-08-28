import base64
import getpass
from pathlib import Path
import keyring
from dotenv import find_dotenv, get_key, load_dotenv, set_key


envfile = find_dotenv()
load_dotenv(envfile)


def set_pwd(pwd_string) -> None:
    keyring.set_password(
        service_name="wiffy_pwd",
        username=getpass.getuser(),
        password=base64.b64decode(pwd_string).decode("utf-8"),
    )


def get_pwd() -> str:
    return keyring.get_password(service_name="wiffy_pwd", username=getpass.getuser())


def save_vk_login(login: str) -> None:
    set_key(envfile, "VK_LOGIN", login)


def save_download_path() -> None:
    if get_key(envfile, "DOWNLOAD_PATH") is None:
        user_downloads_path = Path("~").expanduser() / "Downloads"
        set_key(envfile, "DOWNLOAD_PATH", str(user_downloads_path))
