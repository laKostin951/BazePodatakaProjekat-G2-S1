def radixSort(arr, param):
    # Find the maximum number to know number of digits
    max1 = max(arr, param)
    max_digits = len(str(max1))

    return radix_sort_do(arr, param, max_digits, 1)

def max(arr, parm):
    max = float(arr[0][parm])
    for elm in arr:
        if float(elm[parm]) > max:
            max = float(elm[parm])

    return max

def radix_sort_do(arr, param, max_digits, n):
    if n > max_digits:
        return arr

    buckets = [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        []
    ]

    for elm in arr:
        buckets[round((float(elm[param]) / n) % 10)].append(elm)

    return radix_sort_do(concat(buckets), param, max_digits, n * 10)


def concat(arr):
    return [*arr[0], *arr[1], *arr[2], *arr[3], *arr[4], *arr[5], *arr[6], *arr[7], *arr[8]]

# Driver code to test above
