from random import randrange, shuffle


def quicksort(a):
    def qs(lo, hi):
        if hi - lo <= 1: return
        i, j = partition(lo, hi)
        qs(lo, i)
        qs(j, hi)

    def partition(lo, hi):
        k = randrange(lo, hi)
        pivot = a[k]
        a[lo], a[k] = a[k], a[lo]
        i, m, j = lo, lo + 1, hi
        # a[k] < pivot for k in a[lo: i]
        # a[k] == pivot for k in a[i: m]
        # a[k] > pivot for k in a[j: hi]
        # a[k] is unknown for k in a[m: j]
        while m < j:
            if a[m] < pivot:
                a[i], a[m] = a[m], a[i]
                i += 1
                m += 1
            elif a[m] == pivot:
                m += 1
            elif a[j - 1] > pivot:
                j -= 1
            else:  # a[m] > pivot and a[j - 1] <= pivot
                a[m], a[j - 1] = a[j - 1], a[m]
                j -= 1
        return i, j

    qs(0, len(a))


def quicksort2(a):
    def qs(lo, hi):
        if hi - lo <= 1: return
        i, pivot = lo - 1, a[hi - 1]

        for j in range(lo, hi - 1):
            # all(a[k] < pivot for k in range(lo, i + 1)
            # all(a[k] >= pivot for k in range(i + 1, j)
            if a[j] < pivot:
                i += 1
                a[i], a[j] = a[j], a[i]
        # all(a[k] < pivot for k in range(lo, i + 1)
        # all(a[k] >= pivot for k in range(i + 1, hi - 1)
        i += 1
        a[i], a[hi - 1] = pivot, a[i]
        qs(lo, i)
        qs(i + 1, hi)

    qs(0, len(a))


def quicksort1(a):
    shuffle(a)

    def partition(lo, hi):
        i, pivot = lo, a[lo]
        for j in range(lo + 1, hi):
            # all(a[k] <= pivot for k in range(lo, i + 1)
            # all(a[k] > pivot for k in range(i + 1, j)
            if a[j] <= pivot:
                i += 1
                a[i], a[j] = a[j], a[i]
        # all(a[k] <= pivot for k in range(lo, i + 1)
        # all(a[k] > pivot for k in range(i + 1, hi)
        if i > lo:
            a[i], a[lo] = a[lo], a[i]
        return i

    def qs(lo, hi):
        if hi - lo <= 1: return
        p = partition(lo, hi)
        qs(lo, p)
        qs(p + 1, hi)

    qs(0, len(a))


if __name__ == '__main__':
    a = [1]
    quicksort(a)
    b = [randrange(1, 10) for _ in range(10)]
    quicksort(b)
    c = list(range(10, 0, -1))
    d = [randrange(1, 10) for _ in range(20)]
    quicksort(d)
    print(a, b, c, d, sep='\n')
    e = [randrange(1, 1000001) for _ in range(200000)]
    f = e[:]
    f.sort()
    print(f[:10], f[-10:])
    quicksort(e)
    print(e[:10], e[-10:])
    assert e == f
    e = list(reversed(e))
    print(e[:10], e[-10:])
    quicksort(e)
    print(e[:10], e[-10:])
    g = [randrange(1, 10) for _ in range(100000)]
    quicksort(g)
    print(g[:10], g[-10:])
    # quicksort1(g)
    # print(g[:10],g[-10:])
