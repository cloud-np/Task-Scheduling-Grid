def connect_dummy_nodes(tasks):
    for task in tasks:
        pass
    pass


def get_id_from_name(name):
    flag = False
    str_id = ''
    for i in range(len(name)):
        if name[i] == '_' and name[i + 1].isdigit():
            flag = True
            continue

        if flag:
            str_id += name[i]
    return int(str_id)
