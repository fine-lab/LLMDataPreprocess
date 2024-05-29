import json
import os

# 去重
def deleteDuplicate(l):
    temp = set()
    result = []
    for i in l:
        if not temp.__contains__(str(i.get("conversations"))):
            temp.add(str(i.get("conversations")))
            result.append(i)

    return result

# 获取列表id
def takeId(elem):
    return int(elem.get("id"))

path = "D://aData//JS代码生成//数据处理//脚本定义数据优化20231211//鑫超处理完的数据//数据集-(all_1102_pretty)(无注释)"
files= os.listdir(path) #得到文件夹下的所有文件名称

for file in files:

    # 获取json数据
    with open(path + "//" + file, 'r', encoding='utf-8') as f:
        rows = json.load(f)
    result = deleteDuplicate(rows)
    result.sort(key=takeId, reverse=False)
    f.close()

    with open('D://aData//JS代码生成//数据处理//去重后//数据集-(all_1102_pretty)(无注释)//' + file, 'w', encoding='utf-8') as f2:
        json.dump(result, f2, ensure_ascii=False, indent=4)
    f2.close()
    print(file + " ")
    print(result.__len__())
    print((rows.__len__()-result.__len__()))

