import re


def get_email_regex() -> re.Pattern:
    return re.compile(r"([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+)")


def get_phone_number_regex() -> re.Pattern:
    return re.compile(r"^((8|\+\d{1,3})[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$")


def string_is_email(string: str) -> bool:
    return (
        "@" in string or re.search(r"\.\s+", string) is not None or re.search(r"[A-Za-z]+", string) is not None
    ) and not string.isdigit()
