import time


def process(serialize_list: list):
    year_now = time.localtime().tm_year
    res_dict = {}
    while year_now >= 2017:
        this_year_list = []
        for item in serialize_list:
            if int(item.get('prize_time')[0:4]) == year_now:
                this_year_list.append(
                    {
                        "pid": item.get('pid'),
                        "pictureurl": item.get('pictureurl'),
                        "text": item.get('text')
                    }
                )
        if len(this_year_list):
            res_dict[year_now] = this_year_list
        year_now -= 1
    return res_dict
