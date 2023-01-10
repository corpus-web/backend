import re
from random import shuffle

from ..models import File


def get_essay_list_by_word(word, limitcase=False, randomcase=False, category=1, page=1, per_page=10, window_size=50):
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
        if limitcase:
            position_list = [m.start() for m in re.finditer(" " + word, essay_text)]
        else:
            position_list = [m.start() for m in re.finditer(" " + word, essay_text, re.I)]
        for item in position_list:
            fid = essay.id
            fname = essay.name
            fline = get_line(essay_text, word, window_size, item)
            res_list.append({"fid": fid, "fname": fname, "fline": fline})
            total += 1
        if randomcase:
            shuffle(res_list)
    return {
        "total": total,
        "data": res_list[(int(page) - 1) * int(per_page):int(page) * int(per_page)]
    }


def get_essay_list_by_regex(regex, limitcase=False, category=1, page=1, per_page=10, window_size=50):
    pass


def get_line(text_str, word, window_size, word_index):
    if word_index <= 0:
        return False
    index_l = int(word_index)
    index_r = int(word_index) + len(word)
    while index_l > 0 and int(word_index) - index_l <= int(window_size):
        index_l -= 1
    while index_r < len(text_str) and index_r - word_index - len(word) <= int(window_size):
        index_r += 1
    return text_str[index_l:index_r].replace("\n", " ")
