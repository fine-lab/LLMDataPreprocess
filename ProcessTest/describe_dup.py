import pandas as pd

path = "D:\\aData\\JS代码生成\\测试\\质量检测\\评分过滤_后端脚本\\"
txt = open(path + "最终结果\\评分过滤结果(1742)_脚本描述未去重.txt")
excel = pd.read_excel(path + "过滤去重\\代码质量检测结果_过滤去重.xls")

data = []  # 筛选结果
for line in txt:
    data.append(line.replace("\n", ""))

result = []  # 结果数据
describe = []  # 存储脚本描述
# 脚本描述完全一样（描述为空的除外）的只保留一个
delete_num = 0
for i in excel.values:
    if data.__contains__(i[0]):
        # 描述不重复则加入最终结果
        if not isinstance(i[5], str) or not describe.__contains__(i[5]):
            result.append(i[0])
            describe.append(i[5])
        else:
            print(i)
            delete_num += 1

# 写入文件
f = open(path + "最终结果\\评分过滤结果.txt", "w")
for line in result:
    f.write(line+'\n')
f.close()
