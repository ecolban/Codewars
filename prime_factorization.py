from collections import Counter
from itertools import groupby


def is_prime(n):
    return n == 2 or n & 1 and all(n % f for f in range(3, int(n ** 0.5) + 1, 2))


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


def gen_distinct_prime_factors(n):
    for p, _ in groupby(gen_prime_factors(n)):
        yield p


def prime_factors(n):
    return Counter(gen_prime_factors(n))


def totient(n):
    for p, _ in groupby(gen_prime_factors(n)):
        n = n // p * (p - 1)
    return n


def gcd(a, b):
    while a > 0:
        a, b = b % a, a
    return b


def tower(base, h, m):
    """Return base ** base ** ... ** base, where the height is h, modulo m. """
    base %= m
    if m == 1: return 0
    if h == 0: return 1
    if h == 1: return base
    if h == 2: return pow(base, base, m)
    if h == 3 and base < 8: return pow(base, base ** base, m)
    if h == 4 and base == 2: return 65536 % m
    if h == 5 and base == 2: return pow(2, 65536, m)
    # if T > totient(m) and q, r = divmod(T, totient(m)), then
    # b ** T mod m == b ** (q * totient(m) + r) mod m == b ** (totient(m) + r) mod m,
    k = totient(m)
    r = tower(base, h - 1, k)
    return pow(base, k + r, m)


def power_cycle(base, mod):
    return find_cycle(lambda n: n * base % mod, 1)


def find_cycle(f, start):
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
