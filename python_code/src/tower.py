from itertools import groupby
from math import log


def tower(base, h, m):
    """Returns base ** base ** ... ** base modulo m, where the number
    of occurrences of base is h.
    Note that ** is right-associative.
    base is an int, base > 0,
    h is an int, h > 0,
    m is an int, m > 0 """

    if m == 1:
        return 0
    if base == 1 or h == 0:
        return 1
    # Let exp = tower(base, h - 1), i.e. a tower of height h - 1 (no modulo)
    # If exp >= totient(m) and exp == q * totient(m) + r, where 0 <= r < totient(m)
    # then (base ** exp) % m == (base ** (q * totient(m) + r)) % m == base ** (totient(m) + r)
    tot = totient(m)
    lim = log(tot) / log(base)
    exp = 1
    for i in range(h - 1):
        if exp >= lim:
            # base ** exp >= tot
            break
        exp = base ** exp
    else:
        # base ** exp < tot
        return pow(base, exp, m)

    r = tower(base, h - 1, tot)
    return pow(base, tot + r, m)


def totient(n):
    res = n
    for p, _ in groupby(gen_prime_factors(n)):
        res -= res // p
    return res


def gen_prime_factors(n):
    # Check 2 first
    while n & 1 == 0:
        yield 2
        n >>= 1
    # Check odd factors
    factor, factor_sqr = 3, 9
    while factor_sqr <= n:
        while n % factor == 0:
            yield factor
            n //= factor
        factor += 2
        factor_sqr += factor - 1 << 2
    if n > 1:
        yield n


def power_cycle(base, mod):
    return find_cycle(lambda n: n * base % mod, 1)


def find_cycle(f, start):
    """Returns the start of a cycle, and the cycle length. """
    tortoise, hare = start, f(start)
    while tortoise != hare:
        hare = f(f(hare))
        tortoise = f(tortoise)
    tortoise = start
    hare = f(hare)
    while tortoise != hare:
        tortoise = f(tortoise)
        hare = f(hare)
    tortoise, lamb = f(tortoise), 1
    while tortoise != hare:
        tortoise = f(tortoise)
        lamb += 1
    return hare, lamb


if __name__ == "__main__":
    print([tower(89, i, 100000000000000) for i in range(1, 21)])