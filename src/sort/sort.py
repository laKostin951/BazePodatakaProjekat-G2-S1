def isfloat(x):
    non_numeric_car = [i for i in split(x) if not i.isdigit()]

    if len(non_numeric_car) != 1:
        return False
    if non_numeric_car[0] != '.':
        return False

    return True

def split(word):
    return [char for char in word]


# date-time provera
def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


def sort(data, parm):
    type = get_type(data, parm)

    if type == 1:
        from dataHandler.sort.sorting_alg.merge import merge_sort
        return merge_sort(data, parm)

def get_type(data, parm):
    number_count = 0
    str_count = 0
    date_count = 0
    data_arr = []
    for i in range(0, 100 if len(data) > 100 else len(data)):
        data_arr.append(data[i][parm])

    for elm in data_arr:
        if isfloat(elm) or elm.isnumeric():
            number_count += 1
            continue
        # if all(ord(char) < 128 for char in elm):
        str_count += 1

    if number_count > str_count:
        return 1
    return 2
