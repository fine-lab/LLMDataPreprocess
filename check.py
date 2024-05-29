import json
import os

path = "D://aData//JS代码生成//数据处理//去重后//数据集-(all_1102_pretty)(无注释)"
files= os.listdir(path) #得到文件夹下的所有文件名称

allconversation = set()
dup = 0
for file in files:
    print(file)
    # 获取json数据
    with open(path + "//" + file, 'r', encoding='utf-8') as f:
        rows = json.load(f)
    for row in rows:
        if allconversation.__contains__(str(row.get("conversations"))):
            dup += 1
            print(row.get("id"))
        else:
            allconversation.add(str(row.get("conversations")))
    # result = deleteDuplicate(rows)
    # result.sort(key=takeId, reverse=False)
    f.close()

print(dup)

