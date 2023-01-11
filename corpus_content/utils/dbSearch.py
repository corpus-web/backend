import re
from random import shuffle

from ..models import File


def get_essay_list_by_word(word, limit_case=False, random_case=False, category=1, page=1, per_page=10, window_size=50):
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
        if limit_case:
            position_list = [m.start() for m in re.finditer(" " + word, essay_text)]
        else:
            position_list = [m.start() for m in re.finditer(" " + word, essay_text, re.I)]
        for item in position_list:
            fid = essay.id
            fname = essay.name
            fline = get_line(essay_text, word, window_size, item)
            s_name = format_str(fline)
            res_list.append({"fid": fid, "fname": fname, "fline": fline, "s_name": s_name})
            total += 1
        if random_case:
            shuffle(res_list)
    return {
        "total": total,
        "data": res_list[(int(page) - 1) * int(per_page):int(page) * int(per_page)]
    }


def get_line(text_str, word, window_size, word_index):
    if word_index <= 0:
        return False
    index_l = int(word_index)
    index_r = int(word_index) + len(word)
    while index_l > 0 and int(word_index) - index_l <= int(window_size):
        index_l -= 1
    while index_r < len(text_str) and index_r - word_index - len(word) <= int(window_size):
        index_r += 1
    return text_str[index_l:index_r].replace("\\n", " ").replace("\\r", " ")


def get_frequency_list(word_or_regex, limit_case=False, category=1, query_method=0):
    if int(query_method) == 0:
        if int(category) == 0:
            if limit_case:
                num = File.objects.filter(text__contains=word_or_regex).count()
            else:
                num = File.objects.filter(text__icontains=word_or_regex).count()
        elif int(category) == 1:
            if limit_case:
                num = File.objects.filter(category_id=1, text__contains=word_or_regex).count()
            else:
                num = File.objects.filter(category_id=1, text__icontains=word_or_regex).count()
        else:
            if limit_case:
                num = File.objects.filter(category_id=2, text__contains=word_or_regex).count()
            else:
                num = File.objects.filter(category_id=2, text__icontains=word_or_regex).count()
        return [{"name": word_or_regex, "s_name": word_or_regex, "num": num}]
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
        if limit_case:
            pattern = re.compile(reg)
        else:
            pattern = re.compile(reg, re.I)
        match_list = []
        for essay in query_set:
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
    text = text.replace("_,", "")
    text = text.replace(" ,", ",")
    if text[-1] == " ":
        text = text[:-1]
    if text[-1] == "_":
        text = text[:-1]
    return text
