from itertools import chain, cycle


def gaps(p):
    if p == 2:
        yield 1
        while True:
            yield 2
    elif p == 3:
        yield 1
        yield 2
        while True:
            yield 2
            yield 4
    elif p == 5:
        yield 1
        yield 2
        yield 2
        while True:
            yield 4
            yield
    else:
        return chain((1,), cycle((2,)))


def gen_prime_factors(n):
    """Generate all the prime factors of n in ascending order"""
    g = gaps(5)
    factor = 2
    while factor * factor <= n:
        if n % factor == 0:
            yield factor
            n //= factor
        else:
            factor += next(g)
    if n > 1:
        yield n
