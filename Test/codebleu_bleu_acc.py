import tablib
from codebleu import calc_codebleu
from nltk.translate.bleu_score import sentence_bleu
import pandas as pd

import util.excel_util as ex


def get_indicator(df, path):
    """
    注意：
    1.没有数据流时，要将数据流权重设置为0;
    2.代码分割后不足四个词时，要在weighted_ngram_match_score和ngram_match_score增加参数auto_reweigh=True
    """
    data_list = ex.excel_to_listdict(df)
    header = list(df.columns)
    header = header + list(['acc', 'codebleu', 'bleu', 'weighted_ngram_match_score',
                            'syntax_match_score', 'dataflow_match_score'])
    data = []
    for row in data_list:
        body = []
        candidate = row['predict']
        reference = row['gold']
        for i in row.values():
            body.append(i)
        codebleu = calc_codebleu([reference], [candidate], lang="javascript", weights=(0.25, 0.25, 0.25, 0.25),
                                 tokenizer=None)
        # 注！！！用的时候要把没有数据流情况的返回值改为-1
        if codebleu['dataflow_match_score'] == -1:
            print('没有dataflow_match_score')
            codebleu = calc_codebleu([reference], [candidate], lang="javascript", weights=(1 / 3, 1 / 3, 1 / 3, 0),
                                     tokenizer=None)
        if candidate.strip() == reference.strip():
            acc = 1
        else:
            acc = 0
        body += list([acc, codebleu['codebleu'], codebleu['ngram_match_score'],
                     codebleu['weighted_ngram_match_score'], codebleu['syntax_match_score'],
                     codebleu['dataflow_match_score']])
        data.append(tuple(body))

    data = tablib.Dataset(*data, headers=header)
    open(path + '测试.xlsx', 'wb').write(data.xls)


def get_indicator_sum(df, path, filename):
    """
    注意：
    1.没有数据流时，要将数据流权重设置为0;
    2.代码分割后不足四个词时，要在weighted_ngram_match_score和ngram_match_score增加参数auto_reweigh=True
    """
    acc_list = []
    bleu_list = []
    codebleu_list = []
    data_list = ex.excel_to_listdict(df)
    for i in data_list:
        # if i['type'] != 'test_js_fjbdy.json':
        #     continue
        # if i['id'] == 1215:
        #     acc_list.append(0)
        #     bleu_list.append(0)
        #     codebleu_list.append(0)
        #     continue
        # print(i['id'])
        candidate = i['predict']
        reference = i['gold']
        codebleu = calc_codebleu([reference], [candidate], lang="javascript", weights=(0.25, 0.25, 0.25, 0.25),
                                 tokenizer=None)
        # 注！！！用的时候要把没有数据流情况的返回值改为-1
        if codebleu['dataflow_match_score'] == -1:
            print('没有dataflow_match_score')
            codebleu = calc_codebleu([reference], [candidate], lang="javascript", weights=(1 / 3, 1 / 3, 1 / 3, 0),
                                     tokenizer=None)
        if candidate.strip() == reference.strip():
            acc = 1
            print(i)
        else:
            acc = 0
        acc_list.append(acc)
        bleu_list.append(codebleu['ngram_match_score'])
        codebleu_list.append(codebleu['codebleu'])
        # data.append(body)

    # data = tablib.Dataset(*data, headers=header)
    # open(path + '测试.xlsx', 'wb').write(data.xls)
    result = 'ACC: ' + str((sum(acc_list) / len(acc_list))) \
             + '\nBLEU: ' + str((sum(bleu_list) / len(bleu_list))) \
             + '\nCODEBLEU: ' + str((sum(codebleu_list) / len(codebleu_list)))

    f = open(path + filename + '.txt', "w")
    f.write(result)
    f.close()


def get_prompt(df, path):
    data_list = ex.excel_to_listdict(df)
    header = list(df.columns)
    header.append('prompt')
    data = []
    for row in data_list:
        body = []
        for i in row.values():
            body.append(i)
        body.append('假如你是一个javascript工程师，[预测代码]和[正确代码]，并比较[预测代码]与[正确代码]的差距。\n预测代码：\n'
                     + row['predict'] + '\n正确代码：\n' + row['gold'])
        data.append(tuple(body))
    data = tablib.Dataset(*data, headers=header)
    open(path + '测试.xlsx', 'wb').write(data.xls)


path = "D:\\aData\\基础前端代码生成\\"
# 把Excel文件中的数据读入pandas
filename = 'jcqd_test_1_lite'
df = pd.read_csv(path + filename + '.csv')
# df = pd.read_csv(path + filename + '.csv', encoding='gbk')
get_indicator(df, path)
get_indicator_sum(df, path, filename)
# get_prompt(df, path)

# reference = '  processInstanceEnd(processStateChangeMessage) {}'
# candidate = '  processInstanceEnd(processStateChangeMessage) {}'
# codebleu = calc_codebleu([reference], [candidate], lang="javascript", weights=(1 / 3, 1 / 3, 1 / 3, 0),
#                          tokenizer=None)
# print(codebleu)