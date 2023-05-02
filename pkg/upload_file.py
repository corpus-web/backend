import requests
import os

sub_category_name = "核燃料循环与材料学术"
# folder_name = "J07-Ultrasonics"
url = "http://192.168.31.200:8000/api/corpus/files"
datas = {
    'sub_name': f"{sub_category_name}",
    # 'sub_name': f"{sub_category_name},{folder_name}",
    'category': 2
}
# file_path = f"D:\\web428\\corpus-antconc\\1\\3\\{folder_name}"
file_path = f"D:\\web428\\corpus-antconc\\2\\4"

if __name__ == '__main__':
    tot_201 = 0
    tot_400 = 0
    error_list = []
    for file in os.listdir(file_path):
        file_data = {'file': open(os.path.join(file_path, file), 'rb')}
        res = requests.post(url, files=file_data, data=datas)
        print(res.status_code)
        if res.status_code == 201:
            tot_201 += 1
        else:
            tot_400 += 1
            error_list.append(file)
    print(str(tot_201) + "个成功")
    print(str(tot_400) + "个失败")
    print(error_list)
