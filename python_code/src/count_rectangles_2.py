from itertools import combinations
from random import randrange, choices
from collections import Counter
from time import time

import numpy as np


def count(lines=[]):
    if not lines: return 0

    def rectangle(i1, j1, i2, j2):
        res = lines[i1][j2] == '+' and lines[i2][j1] == '+' \
              and all(c in '-+' for c in lines[i1][j1 + 1:j2]) \
              and all(c in '-+' for c in lines[i2][j1 + 1:j2]) \
              and all(c in '|+' for c in (lines[x][j1] for x in range(i1 + 1, i2))) \
              and all(c in '|+' for c in (lines[x][j2] for x in range(i1 + 1, i2)))
        return res

    return sum(rectangle(i1, j1, i2, j2)
               for i1, line1 in enumerate(lines)
               for j1, c1 in enumerate(line1) if c1 == '+'
               for i2, line2 in enumerate(lines[i1 + 1:], start=i1 + 1)
               for j2, c2 in enumerate(line2[j1 + 1:], start=j1 + 1) if c2 == '+')


def random_input(rows, cols, n=10):
    m = [[' '] * cols for _ in range(rows)]
    while n > 0:
        n -= 1
        left, right = choose_two(cols)
        top, bottom = choose_two(rows)
        m[top][left] = '+'
        m[top][right] = '+'
        m[bottom][left] = '+'
        m[bottom][right] = '+'
        for j in range(left + 1, right):
            m[top][j] = '+' if m[top][j] in '+|' else '-'
            m[bottom][j] = '+' if m[bottom][j] in '+|' else '-'
        for i in range(top + 1, bottom):
            m[i][left] = '+' if m[i][left] in '+-' else '|'
            m[i][right] = '+' if m[i][right] in '+-' else '|'
    return [''.join(row) for row in m]


def choose_two(n):
    m = randrange(n * (n - 1) // 2)
    j = int((1 + (1 + 8 * m) ** 0.5) / 2)
    i = m - j * (j - 1) // 2
    return i, j


def choose_two_2(n):
    i = randrange(n)
    j = randrange(n - 1)
    return (i, j) if i < j else (i, n - 1) if i == j else (j, i)


def choose_k(n, k):
    res, d = [], {}
    for i in range(n - 1, n - k - 1, -1):
        r = randrange(i + 1)
        res.append(d[r] if r in d else r)
        d[r] = d[i] if i in d else i
    res.sort()
    return tuple(res)


if __name__ == '__main__':
    lines = random_input(30, 140, 10)
    print(*lines, sep='\n')
    print(f'Number of rectangles = {count(lines)}')
    # n = 10000 * 45
    #
    # c = Counter(choose_k(10, 2) for _ in range(n))
    # c2 = Counter(choose_two(10) for _ in range(n))
    # c3 = Counter(choose_two_2(10) for _ in range(n))
    # print(f'len(c) = {len(c)}, sum(c.values()) = {sum(c.values())}')
    # print(f'len(c2) = {len(c2)}, sum(c2.values()) = {sum(c.values())}')
    # print(f'len(c3) = {len(c2)}, sum(c2.values()) = {sum(c.values())}')
    # mean = n / 45
    # print(f'mean = {mean}')
    # print((sum(x * x for x in c.values()) / 45 - mean ** 2) ** 0.5)
    # print((sum(x * x for x in c2.values()) / 45 - mean ** 2) ** 0.5)
    # print((sum(x * x for x in c3.values()) / 45 - mean ** 2) ** 0.5)
    # print(c3)
