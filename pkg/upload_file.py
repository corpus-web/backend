import requests
import os

sub_category_name = "核燃料循环与材料学术"
folder_name = ""
url = "http://192.168.31.200:8000/api/query/file/file"
datas = {
    'sub_name': f"{sub_category_name}",
    # 'sub_name': f"{sub_category_name},{folder_name}",
    'category': 2
}
# file_path = f"D:\\web428\\corpus-antconc\\2\\1\\{folder_name}"
file_path = f"D:\\web428\\corpus-antconc\\2\\4"

if __name__ == '__main__':
    tot = 0
    for file in os.listdir(file_path):
        file_data = {'file': open(os.path.join(file_path, file), 'rb')}
        res = requests.post(url, files=file_data, data=datas)
        print(res.status_code)
        tot += 1
    print(str(tot) + "个请求成功发送")
