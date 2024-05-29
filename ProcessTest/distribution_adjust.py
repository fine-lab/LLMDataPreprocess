import pandas as pd
import tablib

path = "D:\\aData\\JS代码生成\\测试\\质量检测\\评分过滤_后端脚本\\过滤去重\\"
interval = 13  # 区间
# 2.把Excel文件中的数据读入pandas
df = pd.read_excel(path + 'API_过滤去重.xls')

header = list(df.columns)
list_dic = []  # excel转list嵌套dict
for i in df.values:  # i 为每一行的value的列表
    a_line = dict(zip(header, i))
    a_line["issue/total"] = a_line["Issues"] / a_line["Total Lines"]
    a_line["code/total"] = a_line["Lines o Code"] / a_line["Total Lines"]
    list_dic.append(a_line)
total_num = len(list_dic)  # 数据总数

arr = [0 for i in range(interval)]  # 计算区间数量
list_interval = [[] for i in range(interval)]  # 按照区间划分存储数据
arr_zero = [0 for i in range(interval)]  # 区间issues为0的数据
for i in list_dic:
    arr[i["Total Lines"] // 100] += 1
    list_interval[i["Total Lines"] // 100].append(i)
    if i["Issues"] == 0:
        arr_zero[i["Total Lines"] // 100] += 1

# for i in range(len(arr)):
#     print(i, arr[i] / sum(arr))
# for i in range(len(arr_zero)):
#     print(i, arr_zero[i] / sum(arr_zero))

# result_1 = []
# result_2 = []
result = []
result_check = [[] for i in range(interval)]
result_not_zero = [0 for i in range(interval)]  # 增加的issue非0数据
result_max_issue = [0 for i in range(interval)]  # issue/total_lines最大值
result_num = total_num * 0.4
for i in range(8):
    # 按照两个元素排序
    list_interval[i].sort(key=lambda x: (x['issue/total'], x['code/total']))
    # 按照数据总集分布获取数据数量
    num = int(arr[i] / sum(arr) * result_num)
    # 0区间的数据手动删除2条
    # if i == 0:
    #     num -= 2
    result_max_issue[i] = list_interval[i][num - 1]["issue/total"]
    for j in range(num):
        result_check[list_interval[i][j]["Total Lines"] // 100].append(list_interval[i][j])
        if not list_interval[i][j]["Issues"] == 0:
            result_not_zero[list_interval[i][j]["Total Lines"] // 100] += 1
        result.append(list_interval[i][j]["File Name"])
        # 分为核心1和核心2
        # if list_[i][j]["Type"] == 1:
        #     result_1.append(list_[i][j]["File Name"])
        # else:
        #     result_2.append(list_[i][j]["File Name"])

print(sum(result_not_zero))
# 查看分布
for i in range(len(result_check)):
    print(i, (len(result_check[i])) / result_num, result_not_zero[i], result_max_issue[i])

# 过滤情况
header = ["区间", "处理前区间占比", "处理后区间占比", "增加issue非0数量", "issue/total_lines最大值"]
data = []
for i in range(len(result_check)):
    body = []
    body.append(str(i * 100) + '-' + str((i + 1) * 100))
    body.append(arr[i] / total_num)
    body.append((len(result_check[i])) / result_num)
    body.append(result_not_zero[i])
    body.append(result_max_issue[i])
    data.append(tuple(body))
data = tablib.Dataset(*data, headers=header)
open(path + 'API评分过滤情况.xls', 'wb').write(data.xls)
# 写入文件
f = open(path + "API.txt", "w")
for line in result:
    f.write(line+'\n')
f.close()
# f1 = open(path + "核心1.txt", "w")
# for line in result_1:
#     f1.write(line+'\n')
# f1.close()
# f2 = open(path + "核心2.txt", "w")
# for line in result_2:
#     f2.write(line+'\n')
# f2.close()
