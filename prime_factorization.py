from itertools import groupby


def gen_prime_factors(n):
    """Generate all the prime factors of n in ascending order"""

    # Check 2 first
    while n & 1 == 0:
        yield 2
        n >>= 1
    # Check odd factors
    factor, factor_sqr = 3, 9
    while factor_sqr <= n:
        if n % factor == 0:
            yield factor
            n //= factor
        else:
            factor, factor_sqr = factor + 2, factor_sqr + (factor + 1 << 2)
    if n > 1:
        yield n


def prime_factors(n):
    return [(p, sum(1 for _ in g)) for p, g in groupby(gen_prime_factors(n))]


def is_prime(n):
    return 1 < n == next(gen_prime_factors(n))


def gen_distinct_prime_factors(n):
    for p, _ in groupby(gen_prime_factors(n)):
        yield p


def totient(n):
    for p, _ in groupby(gen_prime_factors(n)):
        n = n // p * (p - 1)
    return n


def smallest_prime_factor(n):
    """Returns the smallest prime factor of n
    n: An int >= 2
    Raises a ValueError is n < 2
    """
    return next(p for p in gen_prime_factors(n))


def largest_prime_factor(n):
    """Returns the largest prime factor of n
    n: An int >= 2
    Raises a ValueError is n < 2
    """
    return max(p for p in gen_distinct_prime_factors(n))


def gcd(a, b):
    while a > 0:
        a, b = b % a, a
    return b


def tower(base, h, m):
    """Returns base ** base ** ... ** base modulo m, where the number of occurrences of base is h.
    Note that ** is right-associative.
    base is an int, base > 0,
    h is an int, h > 0,
    m is an int, m > 0
    """
    if m == 1:
        return 0
    if h == 1:
        return base % m
    tot = totient(m)
    r = tower(base, h - 1, tot)
    return pow(base, r if r else tot, m)


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
