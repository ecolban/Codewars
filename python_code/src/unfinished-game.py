import sys
from functools import lru_cache, reduce
from itertools import product
from math import exp, gcd, log, ceil
from operator import mul


def divide_pot1(score):
    """Uses recursion and may result in stack overflow."""

    num_players = len(score)

    @lru_cache(maxsize=None)
    def h(score_):
        e = sum(score_) - num_players
        distr = [[num_players ** e if j == i else 0 for j in range(len(score_))] if s - 1 == 0
                 else h(tuple(s_ - 1 if i == j else s_ for j, s_ in enumerate(score_)))
                 for i, s in enumerate(score_)]
        return [sum(a) for a in zip(*distr)]

    preliminary_result = h(tuple(score))
    d = reduce(gcd, preliminary_result)
    return [x // d for x in preliminary_result]


def matrix_get(m, t):
    """Returns m[t[0]][t[1]]...[t[-1]]"""
    for i in t:
        m = m[i]
    return m


def matrix_set(m, t, v):
    """Same effect as m[t[0]][t[1]]...[t[-1]] = v"""
    m = matrix_get(m, t[:-1])
    m[t[-1]] = v


def divide_pot2(dimensions):
    """Builds an N-dimensional "Pascal triangle" using iteration."""
    N = len(dimensions)

    def initialize_matrix(dims):
        return None if not dims else [initialize_matrix(dims[1:]) for _ in range(dims[0] + 1)]

    pascal = initialize_matrix(dimensions)
    for t in product(*(range(d + 1) for d in dimensions)):
        s = sum(e <= 0 for e in t)
        if s <= 1:
            v = ([N ** (sum(t) - N + 1) if e == 0 else 0 for e in t] if s == 1
                 else [sum(a) for a in zip(*(matrix_get(pascal, [e_ - 1 if i == j else e_ for j, e_ in enumerate(t)])
                                             for i, e in enumerate(t) if e > 0))])
            matrix_set(pascal, t, v)
    prelim_result = matrix_get(pascal, dimensions)
    d = reduce(gcd, prelim_result)
    return [e // d for e in prelim_result]


# def test():
#     from fractions import Fraction
#     a = Fraction(1, 2)


if __name__ == '__main__':
    m = 100_000
    n = 2
    k = min(ceil(exp(log(m) / n)), 100)
    # pos = [randrange(max(1, k - 8), k + 1) for _ in range(n)]
    # pos = [3, 8, 10, 4, 9, 11]
    # pos = [24, 40, 99]
    # pos = [10, 10, 1]
    pos = [5, 3, 2]
    print(pos)
    print(reduce(mul, pos))
    solution = divide_pot2(pos)
    assert reduce(gcd, solution) == 1
    print(solution)
    print([e / sum(solution) for e in solution])
    # print(divide_points(pos))

    # test()
    print('fractions' in sys.modules)
    print(sys.getrecursionlimit())
