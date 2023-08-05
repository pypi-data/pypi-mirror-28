import re

regex_has_some_number = re.compile(r"(\d)")
regex_has_some_letter = re.compile(r"([A-z])")
regex_is_valid_email = re.compile(r"^[^\.,,][\w+!]+@(?:[A-z0-9]+\.)+[A-z]{1,6}$")


def has_some_number(text):
    return bool(regex_has_some_number.search(text))


def has_some_letter(text):
    return bool(regex_has_some_letter.search(text))


def is_valid_email(email):
    return bool(regex_is_valid_email.search(email))