import json
import tablib
import os

path = "D://aData//JS代码生成//数据处理//脚本定义数据优化20231211//匹配结果_脚本1_核心1"
files= os.listdir(path) #得到文件夹下的所有文件名称

allinfo = []
for file in files:
    if file.endswith("AllInfo.json"):
        allinfo.append(file)

# 获取json数据
with open(path + "//" + allinfo[0], 'r', encoding='utf-8') as f:
    rows = json.load(f)

# 将json中的key作为header, 也可以自定义header（列名）
header = []
header.append("fileName")
for i in rows.keys():
    header.append(i)
header.append("A")
header.append("B")

data = []
keyEqual = set()
# 循环里面的字典，将value作为数据写入进去
for file in allinfo: #遍历文件夹
    # if file.endswith("AllInfo.json"): #判断是否是AllInfo
    with open(path + "//" + file, 'r', encoding='utf-8') as f:
        rows = json.load(f)
    body = []
    body.append(file)
    for v in rows.values():
        body.append(v)
    # A类
    if(keyEqual.__contains__(rows.get("方法的功能说明"))):
        body.append(1)
    else:
        keyEqual.add(rows.get("方法的功能说明"))
        body.append(0)
    # B类
    if(rows.get("方法的功能说明") == rows.get("方法名称")):
        body.append(1)
    else:
        body.append(0)
    data.append(tuple(body))

data = tablib.Dataset(*data,headers=header)

open('data.xls', 'wb').write(data.xls)

