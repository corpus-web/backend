import os
import re

from corpus_content.models import ArticlePost
from corpus_web.settings import BASE_DIR

from random import shuffle


def search(word_str: str, window_size: int, current_page: int, max_num: int, category: int, limitcase=False,
           randomcase=False):
    if int(category) == 0:
        query_set = ArticlePost.objects.all()
    else:
        query_set = ArticlePost.objects.filter(category=category)
    res_list: list = []
    total = 0
    for essay in query_set:
        essay_path = r"{}".format(str(BASE_DIR) + "/media/{}".format(str(essay.file)))
        with open(essay_path, 'r', encoding='latin-1') as f:
            essay_text = f.read()
        if limitcase:
            position_list = [m.start() for m in re.finditer(" " + word_str, essay_text)]
        else:
            position_list = [m.start() for m in re.finditer(" " + word_str, essay_text, re.I)]
        for i in position_list:
            fid = essay.id
            fname = os.path.basename(str(essay.file))
            fline = get_line(essay_text, word_str, window_size, i)
            res_list.append({"id": fid, "fname": fname, "fline": fline})
            total += 1
    if randomcase:
        shuffle(res_list)
    return {"total": total, "data": res_list[(int(current_page) - 1) * int(max_num):int(current_page) * int(max_num)]}


def get_line(text_str: str, word_str: str, window_size: int, word_index: int):
    if word_index <= 0:
        return False
    index_l: int = word_index
    index_r: int = word_index + len(word_str)
    while index_l > 0 and word_index - index_l <= int(window_size):
        index_l -= 1
    while index_r < len(text_str) and index_r - word_index - len(word_str) <= int(window_size):
        index_r += 1
    return text_str[index_l:index_r].replace("\n", " ")


def get_words(essay, text_str: str, word_list: list, words_all_dict: dict, words_dict: dict, word_index):
    index_l = word_index + 1
    index_r = word_index + 1
    while index_r < len(text_str) and text_str[index_r] not in ["\r", "\n", "\t", " "]:
        index_r += 1
    word = text_str[index_l:index_r]
    if word not in words_all_dict.keys():
        words_all_dict[word] = 1
    else:
        words_all_dict[word] = int(words_all_dict[word]) + 1
    if word not in word_list:
        word_list.append(word)
        words_dict[os.path.basename(str(essay.file))] = [word, index_l]
    else:
        words_dict[os.path.basename(str(essay.file))].append(index_l)
    return word


def search_new(old_word_str: str, category: int = 0, limitcase=False):
    word_str = ' ' + old_word_str
    if int(category) == 0:
        query_set = ArticlePost.objects.all()
    else:
        query_set = ArticlePost.objects.filter(category=category)
    words_all_dict: dict = {}
    words_all_list: list = []
    res_list = []
    for essay in query_set:
        words_dict = {}
        essay_path = r"{}".format(str(BASE_DIR) + "/media/{}".format(str(essay.file)))
        with open(essay_path, 'r', encoding='latin-1') as f:
            essay_text = f.read()
        if limitcase:
            position_list = [m.start() for m in re.finditer(word_str, essay_text)]
        else:
            position_list = [m.start() for m in re.finditer(word_str, essay_text, re.I)]
        if len(position_list) > 0:
            word_list = []
            for i in position_list:
                get_words(essay, essay_text, word_list, words_all_dict, words_dict, int(i))
            res_list.append(words_dict)
    for k in words_all_dict:
        words_all_list.append({'name': k, 'num': words_all_dict[k]})
    return res_list, words_all_list
