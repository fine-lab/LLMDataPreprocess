def list_to_txt(file, result):
    f = open(file, "w")
    for line in result:
        f.write(line + '\n')
    f.close()


def txt_to_list(file):
    result = []
    f = open(file, 'r')
    for i in f:
        result.append(i.replace('\n', ''))
    return result