def bisect_smallest(items, item):
    i, j = -1, len(items)
    while j - i > 1:
        m = (i + j) // 2
        if items[m] < item:
            i = m
        else:
            j = m
    return j


if __name__ == "__main__":
    lst = [2, 5, 5, 5, 8, 8]
    assert bisect_smallest(lst, 1) == 0
    assert bisect_smallest(lst, 2) == 0
    assert bisect_smallest(lst, 5) == 1
    assert bisect_smallest(lst, 6) == 4
    assert bisect_smallest(lst, 8) == 4
    assert bisect_smallest(lst, 9) == 6
    assert bisect_smallest([], 9) == 0
    assert bisect_smallest([1], 9) == 1
    assert bisect_smallest([9], 9) == 0

