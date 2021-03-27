def merge_sort(arr, parm):
    if len(arr) <= 1:
        return arr

    mid = round(len(arr) // 2)

    left_arr = arr[0: mid]
    right_arr = arr[mid:]

    return merge(merge_sort(left_arr, parm), merge_sort(right_arr, parm), parm)


def merge(left_arr, right_arr, parm):
    left_index = 0
    right_index = 0
    sorted_slice_of_arr = []
    while left_index < len(left_arr) and right_index < len(right_arr):
        if float(left_arr[left_index][parm]) < float(right_arr[right_index][parm]):
            sorted_slice_of_arr.append(left_arr[left_index])
            left_index += 1
        else:
            sorted_slice_of_arr.append(right_arr[right_index])
            right_index += 1

    return [*sorted_slice_of_arr, *left_arr[left_index:], *right_arr[right_index:]]
