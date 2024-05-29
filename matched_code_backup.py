import json
import tablib
import os

def takeKeyFileName(elem):
    return elem.replace("_AllInfo", "")

path = "D://aData//JS代码生成//数据处理//脚本定义数据优化20231211//匹配结果_脚本1_核心1"
files= os.listdir(path) #得到文件夹下的所有文件名称

# key和value的文件分别存放，顺序对应
keys = []
values = []
for file in files:
    if file.endswith("AllInfo.json"):
        values.append(file)
    else:
        keys.append(file)
keys.sort()
values.sort(key=takeKeyFileName)

# 循环里面的字典，将value作为数据写入进去
machedCode = {}
for i in range(len(keys)): #遍历文件夹
    with open(path + "//" + keys[i], 'r', encoding='utf-8') as f1:
        keyRow = json.load(f1)
    key = keyRow.get("方法名称") + "_" + keyRow.get("方法搜索的关键字") + "_" + keyRow
    with open(path + "//" + values[i], 'r', encoding='utf-8') as f2:
        keyRow = json.load(f2)

    f1.close()
    f2.close()

