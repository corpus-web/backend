import requests
import os

category = 2
url = "http://127.0.0.1:8000/api/corpus/files"
# sub_sub_name = "J07-Ultrasonics"
# file_path = "K:\\项目\\语料库\\船舶与海洋工程学术英语语料库\\船舶与海洋工程学术英语语料库\\水声工程学术英语语料库\\不含语步标注版\\词性赋码\\" + sub_sub_name
datas = {
    # 'sub_name': "船舶与海洋结构物设计制造学术," + sub_sub_name
    'sub_name': "核燃料循环与材料学术"
}
file_path = "K:\\项目\\语料库\\核学科学术英语语料库\\核学科学术英语语料库\\核燃料循环与材料学术英语语料库"

if __name__ == '__main__':
    tot = 0
    for file in os.listdir(file_path):
        file_data = {'file': open(os.path.join(file_path, file), 'rb')}
        res = requests.post(url, files=file_data, data=datas)
        print(res.status_code)
        tot += 1
    print(str(tot) + "个请求成功发送")
