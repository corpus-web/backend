import re


def check_date_format(date_str: str) -> bool:
    correct_form = re.compile("^((19[2-9]\d{1})|(20[0-9]{2}))\-((0?[1-9])|(1[0-2]))\-((0?[1-9])|([1-2][0-9])|30|31)$")
    if not date_str:
        return False
    if not correct_form.match(date_str):
        return False
    return True
