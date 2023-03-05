import re
from random import shuffle

from ..models import File


def get_essay_list_by_word(word, limit_case="false", random_case="false", category=1, page=1, per_page=10,
                           window_size=50):
    reg = r"\W{}[^a-zA-Z]".format(word)
    if int(category) == 0:
        query_set = File.objects.all()
    elif int(category) == 1:
        query_set = File.objects.filter(category_id=1)
    else:
        query_set = File.objects.filter(category_id=2)
    res_list = []
    total = 0
    if not query_set:
        return False
    for essay in query_set:
        essay_text = essay.text
        if limit_case == "true":
            position_list = [m.start() for m in re.finditer(reg, essay_text)]
        else:
            position_list = [m.start() for m in re.finditer(reg, essay_text, re.I)]
        for item in position_list:
            fid = essay.id
            fname = essay.name
            fcategory = essay.category_id
            fline = get_line(essay_text, word, window_size, item, fcategory)
            s_name = format_str(fline)
            res_list.append({"fid": fid, "fname": fname, "fline": fline, "s_name": s_name})
            total += 1
        if random_case == "true":
            shuffle(res_list)
    return {
        "total": total,
        "data": res_list[(int(page) - 1) * int(per_page):int(page) * int(per_page)]
    }


def get_line(text_str, word, window_size, word_index, category):
    if word_index <= 0:
        return False
    if int(category) == 1:
        window_size = int(window_size) + 10
    index_l = int(word_index)
    index_r = int(word_index) + len(word)
    while index_l > 0 and int(word_index) - index_l <= int(window_size):
        index_l -= 1
    while index_r < len(text_str) and index_r - word_index - len(word) <= int(window_size):
        index_r += 1
    return text_str[index_l:index_r].replace("\\n", " ").replace("\\r", " ")


def get_frequency_list(word_or_regex, limit_case="false", category=1, query_method=0):
    total = 0
    reg = r"\W{}[^a-zA-Z]".format(word_or_regex)
    if int(query_method) == 0:
        if int(category) == 0:
            if limit_case == "true":
                query_set = File.objects.filter(text__regex=reg)
                for essay in query_set:
                    lst = re.findall(reg, essay.text)
                    total += len(lst)
            else:
                query_set = File.objects.filter(text__iregex=reg)
                for essay in query_set:
                    lst = re.findall(reg, essay.text)
                    total += len(lst)
        else:
            if limit_case == "true":
                query_set = File.objects.filter(category_id=int(category), text__regex=reg)
                for essay in query_set:
                    lst = re.findall(reg, essay.text)
                    total += len(lst)
            else:
                query_set = File.objects.filter(category_id=int(category), text__iregex=reg)
                for essay in query_set:
                    lst = re.findall(reg, essay.text)
                    total += len(lst)
        return [{"name": word_or_regex, "s_name": word_or_regex, "num": total}]
    else:
        reg = r"{}".format(word_or_regex)
        if int(category) == 0:
            query_set = File.objects.filter(text__iregex=reg)
        elif int(category) == 1:
            query_set = File.objects.filter(category_id=1, text__iregex=reg)
        else:
            query_set = File.objects.filter(category_id=2, text__iregex=reg)
        form_list = []
        form_count_dict = {}
        if limit_case == "true":
            pattern = re.compile(reg)
        else:
            pattern = re.compile(reg, re.I)
        for essay in query_set:
            match_list = []
            m = pattern.finditer(essay.text)
            for finditer in m:
                match_list.append(finditer.group())
            for item in match_list:
                if item in form_list:
                    form_count_dict[item] += 1
                else:
                    form_list.append(item)
                    form_count_dict[item] = 1
        res_list = []
        for i in form_list:
            s_name = format_str(i)
            res_list.append({"name": i, "s_name": s_name, "num": form_count_dict[i]})
        return res_list


def format_str(text):
    text = str(text)
    if text[-1] != " ":
        text += " "
    pattern = re.compile(r"_\w+\s")
    m = pattern.finditer(text)
    content = []
    for finditer in m:
        content.append(finditer.group())
    for i in content:
        text = text.replace(i, " ")
    rep_list = ["\\xce", "\\x94", "\\xe2", "\\xaf", "\\x93", "\\x80", "\\xb2", "\\xef", "\\xac", "\\x02", "\\x81",
                "\\x9c", "\\x9d", "\\x82", "\\x84", "\\xcf", "\\x89", "\\xbc", "\\x8b", "\\x85", "\\x88", "\\x92",
                "\\xa5", "\\xa6", "\\x91", "\\x9b", "\\xbd", "\\xf0", "\\x96", "\\x8f", "\\x86", "\\xb1", "\\x9d",
                "\\xa1", "\\x83", "\\x90", "\\rb7", "\\x99", "\\xb7", "\\xc3", "\\xa8", "\\x97", "\\xc5", "\\x98",
                "\\xb4", "\\x87", "\\xcb", "\\xa2", "\\x8a", "\\xa4", "\\xcc", "\\xc2", "\\xb0", "\\x9a"]
    for i in rep_list:
        if i in text:
            text = text.replace(i, "")
    text = text.replace("_,", "")
    text = text.replace(" ,", ",")
    text = text.replace("  ", " ")
    text = text.replace("_(", "")
    text = text.replace("_)", "")
    text = text.replace(" )_", "")
    text = text.replace("(_", "")
    text = text.replace(" .", ".")
    text = text.replace(" ;_:", ":")
    text = text.replace("_:", "")
    if text[-1] == " ":
        text = text[:-1]
    if text[-1] == "_":
        text = text[:-1]
    return text
