import keyring
import getpass
import base64
from dotenv import load_dotenv, find_dotenv, set_key


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
