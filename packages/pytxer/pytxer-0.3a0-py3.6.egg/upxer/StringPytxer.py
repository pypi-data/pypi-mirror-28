import re

regex_first_letter_lowercase = re.compile(r"(^[^A-Z])|\w([A-Z])")
regex_capitalize_name = re.compile(r"\b[^\s^A-Z]")
regex_abbreviate_name = re.compile(r"\s(\w{1})\w+")


def is_uncapitalize(text):
    return bool(regex_first_letter_lowercase.search(text))


def is_uncapitalize_name(name):
    return bool(regex_capitalize_name.search(name))


def capitalize(text):
    if is_uncapitalize(text):
        return text[:1].upper() + text[1:].lower()
    else:
        return text


def capitalize_list_of_strings(list_strings):
    return [capitalize(word) for word in list_strings]


def list_to_string(list):
    return " ".join(str(x) for x in list)


def capitalize_name(name):
    if is_uncapitalize_name(name):
        list_of_substrings = name.split()

        list_of_substrings_capitalize = [
            capitalize(word) for word in list_of_substrings]

        return list_to_string(list_of_substrings_capitalize)
    else:
        return name


def abbreviate_name(name, max_len=12):
    if len(name) > max_len:

        string_abbreviate_name = regex_abbreviate_name.sub(r" \1.", name)

        string_splitted = string_abbreviate_name.lower().split()

        return list_to_string(capitalize_list_of_strings(string_splitted))

    else:
        return name