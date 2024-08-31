from itertools import product
from math import factorial, gcd, prod


def helper(num, *nums):
    return sum(factorial(sum(t)) // prod(map(factorial, t)) * len(t) ** (num + sum(nums) - sum(t))
               for t in product((num - 1,), *map(range, nums)))


def divide_pot(num, wins):
    res = [num - win for win in wins]
    res = [helper(res[i], *res[:i], *res[i + 1:]) for i in range(len(res))]
    d = gcd(*res)
    return [x // d for x in res]

