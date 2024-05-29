import util.excel_util as ex

import pandas as pd
import json

path = "D:\\aData\\JS代码生成\\数据优化\\"
# 把Excel文件中的数据读入pandas
filename = path + '脚本定义_新增_2'
df = pd.read_excel(filename + '.xls')
data = ex.excel_to_listdict(df)

result = []
template = '请你以javascript工程师的身份通读[原始代码]及[相关说明]，根据代码上下文，告诉我在[原始代码]的[光标位置]适合插入的代码，不要给我多余的内容\n\n\n' \
           '相关说明：该脚本类型为：【脚本类型】，该脚本描述为：【脚本描述】\n\n' \
           '原始代码：\n' \
           '【原始代码】'


def standard_new():
    for i in range(len(data)):
        if i == 18:
            print('1')
        print(i)

        r = {'id': str(i)}
        # 获取conversations
        conversations = []

        c_human = {'from': 'human'}
        prompt = json.loads(data[i]['prompt'])
        c_human['value'] = prompt[0]['content']
        conversations.append(c_human)

        c_gpt = {'from': 'gpt', 'value': data[i]['gold']}
        conversations.append(c_gpt)

        r['conversations'] = conversations
        result.append(r)

    with open(filename + '.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    f.close()


def standard():
    for i in range(len(data)):
        r = {'id': str(i)}
        # 获取conversations
        conversations = []

        c_human = {'from': 'human'}
        value_human = template.replace('【脚本类型】', data[i]['脚本类型']).replace('【原始代码】', data[i]['原始代码'])
        if not isinstance(data[i]['脚本描述'], str):
            value_human = value_human.replace('【脚本描述】', ' ')
        else:
            value_human = value_human.replace('【脚本描述】', data[i]['脚本描述'])
        c_human['value'] = value_human
        conversations.append(c_human)

        c_gpt = {'from': 'gpt', 'value': data[i]['插入代码']}
        conversations.append(c_gpt)

        r['conversations'] = conversations
        result.append(r)

    with open(filename + '.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    f.close()


standard_new()