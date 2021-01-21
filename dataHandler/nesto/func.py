
def format_dict(item):
    s = ''
    keys = item.keys()
    values = item.values()

    for key, value in zip(keys, values):
        s += f" {key} : {value}\n"

    return s