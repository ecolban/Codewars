from collections import defaultdict
from functools import reduce
from operator import mul


def digits(n):
    while n > 0:
        n, d = divmod(n, 10)
        yield d


def decomp(n):
    res = defaultdict(int)
    for d in str(n):
        if d == '4':
            res['2'] += 2
        elif d == '6':
            res['2'] += 1
            res['3'] += 1
        elif d == '8':
            res['2'] += 3
        elif d == '9':
            res['3'] += 2
        elif d == '1':
            pass
        else:
            res[d] += 1
    return res


def persistence(n):
    while n >= 10:
        print(sorted(decomp(n).items()), n)
        n = reduce(mul, digits(n))
    print(n)


if __name__ == '__main__':
    persistence(4996238671872)
    persistence(3778888999)
    persistence(438939648)
    persistence(26888999)
    persistence(4478976)
    persistence(2677889)
    persistence(338688)
    persistence(238889)
    persistence(27648)
    persistence(23788)
    persistence(2688)
