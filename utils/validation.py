import re

from utils.user_data import get_pwd


def get_email_regex() -> re.Pattern:
    return re.compile(r"([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+)")


def get_phone_number_regex() -> re.Pattern:
    return re.compile(r"^((8|\+\d{1,3})[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$")


def string_is_email(string: str) -> bool:
    return (
        "@" in string or re.search(r"\.\s+", string) is not None or re.search(r"[A-Za-z]+", string) is not None
    ) and not string.isdigit()


def validate_user_data(login: str) -> None:
    pwd = get_pwd()
    email_regex = get_email_regex()
    phone_number_regex = get_phone_number_regex()

    if not login or not pwd:
        raise ValueError("Login and/or password are not specified. Please, try again.")
    if string_is_email(string=login):
        if not email_regex.match(login):
            raise ValueError("Email is incorrect. Please, try again.")
    else:
        if not phone_number_regex.match(login):
            raise ValueError("Phone number is incorrect. Please, try again.")
