from functools import cache
from itertools import combinations, zip_longest
from math import factorial


def get_base_set_1(limit, args):
    dgts = [digits(i) for i in args]
    res = set()
    idx = 0
    while len(res) < limit:
        d = next(dgts[idx], None)
        if d is not None:
            res.add(d)
        idx = (idx + 1) % len(args)
    return res


def get_base_set(limit, args):
    ds, res = (int(d) for t in zip_longest(*(str(n) for n in args)) for d in t if d is not None), set()
    while len(res) < limit:
        res.add(next(ds))
    return res


def digits(n):
    b = 1
    while b <= n: b *= 10
    while b > 1:
        b //= 10
        d, n = divmod(n, b)
        yield d


def gta_1(limit, *args):
    base_set = get_base_set(limit, args)
    return sum(sum(sum(c) for c in combinations(base_set, i)) * factorial(i) for i in range(1, limit + 1))


def gta_2(limit, *args):
    base_set = get_base_set(limit, args)
    limit_fact = factorial(limit - 1)
    return sum(base_set) * sum(limit_fact // factorial(k) * (limit - k) for k in range(limit))


def a_001339(n: int) -> int:
    @cache
    def p(n, k):
        return (
            1 if k == 0 else
            0 if k > n else
            (k + 1) * p(n - 1, k - 1) + p(n - 1, k)
        )

    return sum(p(n, k) for k in range(n + 1))


A001339 = [1, 3, 11, 49, 261, 1631, 11743, 95901, 876809, 8877691]  # https://oeis.org/A001339


def gta(n: int, *args: list[int]) -> int:
    """
    First, this function determines a base set of digits by taking the first `n` digits of the numbers in `args` in a
    round-robin fashion. Then, it sums up the digits across all arrangements of the base set, referred to as the "grand
    total", and returns this sum. (An arrangement is a permutation of a subset of the base set. There are `choose(n, k)`
    subsets of size `k`, and `factorial(k)` permutations of each such subset. We can sum `factorial(k) * choose(n, k)`
    for `k = 0,..,n` to get the number of all arrangements of the base set.)

    If we fix one digit `d` of the base set, there are `choose(n - 1, k - 1)` subsets of the base set of size `k` that
    contain `d` and `factorial(k)` permutations of each such subset. We can sum `factorial(k) * choose(n - 1, k - 1)`
    for `k = 1,..,n` to get the number of all arrangements that contain `d`. Since `d` occurs exactly once in each of
    these arrangements, this sum is also the number of occurences of `d` in all arrangements of the base set. This sum
    equals `A001339[n - 1]` (see https://oeis.org/A001339).

    Instead of adding up all occurences of `d` across all arrangements, we can count the number of times `d` occurs in
    all arrangements and multiply that number by `d`, which yields `d * A001339[n - 1]`. Since all digits in the base
    set occur the same number of times, the grand total equals `sum(base_set) * A001339[n - 1]`.

    :param n: the number of elements in the base set.
    :param args: numbers from which the digits in the base set are extracted. These numbers contain at least n distinct digits.
    :return: Returns the grand total of the base set.
    """
    dgts = (int(d) for t in (zip_longest(*(str(n) for n in args))) for d in t if d is not None)
    base_set = set()
    while len(base_set) < n:
        base_set.add(next(dgts))
    return sum(base_set) * A001339[n - 1]


if __name__ == '__main__':
    print(f'A001339 = [{", ".join(str(a_001339(n)) for n in range(10))}, ...]')
    n, args = 10, [1427, 205, 3637, 89]
    print(f'gta{n, *args} = {gta(n, *args)}')
