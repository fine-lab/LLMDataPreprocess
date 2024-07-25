import json


def read_jsonl(file_name):
    """
    参数：
      file_name：jsonl格式的文件名，带路径。

    函数作用：读取文件.jsonl
    """
    contents = []
    with open(file_name, mode='r', encoding='UTF-8') as file_js:
        for line in file_js.readlines():
            dic = json.loads(line)
            contents.append(dic)
    return contents


def dict2json(file_path, dic_list):
    with open(file_path + 'test_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(dic_list, json_file, ensure_ascii=False, indent=4)
