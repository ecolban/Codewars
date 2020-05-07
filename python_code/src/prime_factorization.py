from collections import Counter
from functools import reduce
from itertools import chain
from itertools import cycle, count
from itertools import groupby
from itertools import product
from operator import mul


def gen_prime_factors(n):
    """Generate all the prime factors of n in ascending order"""
    gaps = chain((1, 2, 2, 4), cycle((2, 4, 2, 4, 6, 2, 6, 4, 2, 4, 6, 6, 2, 6, 4, 2,
                                      6, 4, 6, 8, 4, 2, 4, 2, 4, 8, 6, 4, 6, 2, 4, 6,
                                      2, 6, 6, 4, 2, 4, 6, 2, 6, 4, 2, 4, 2, 10, 2, 10)))
    factor = 2
    while factor * factor <= n:
        if n % factor == 0:
            yield factor
            n //= factor
        else:
            factor += next(gaps)
    if n > 1:
        yield n


def prime_factors(n):
    """Returns a list of pairs in ascending order where the first
    element of each pair is a prime, and the second element is the
    number of times the prime divides n.
    >>> prime_factors(360)
    [(2, 3), (3, 2), (5, 1)]

    """

    return [(p, sum(1 for _ in g)) for p, g in groupby(gen_prime_factors(n))]


def totient(n):
    """Euler's totient function, a.k.a. Euler's phi funtion.
    Returns the number of integers between 1 and n that are coprime
    with n. For example: totient(60) = 16. The 16 numbers that coprime
    with 60 are: 1, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 49,
    53, 59
    >>> totient(60)
    16
    """

    for p, _ in groupby(gen_prime_factors(n)):
        n -= n // p
    return n


def prod(nums):
    return reduce(mul, nums)


def divisor_count(n):
    """Returns the number of distinct divisors of n, including 1 and n.
    >>> divisor_count(12)
    6
    >>> divisor_count(60)
    12
    >>> divisor_count(2 * 3**4 * 5**6)
    70
    """
    return prod(p + 1 for p in Counter(gen_prime_factors(n)).values())


def divisors(n):
    """
    :param n an int greater than 1
    :returns a sorted list of all the divisors of n, including 1 and n.
    >>> divisors(12)
    [1, 2, 3, 4, 6, 12]
    >>> divisors(60)
    [1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60]
    >>> divisors(100)
    [1, 2, 4, 5, 10, 20, 25, 50, 100]
    """
    primes, powers = zip(*((p, sum(1 for _ in g)) for p, g in groupby(gen_prime_factors(n))))
    return sorted(prod(f ** p for f, p in zip(primes, ps)) for ps in product(*(range(power + 1) for power in powers)))


def is_prime(n):
    """:returns True if n is a prime number, False otherwise.
    >>> is_prime(43)
    True
    >>> is_prime(45)
    False
    """
    return 1 < n == next(gen_prime_factors(n))


def smallest_prime_factor(n):
    """Returns the smallest prime factor of n
    n: An int >= 2
    Raises a StopIteration if n < 2
    >>> smallest_prime_factor(77)
    7
    >>> smallest_prime_factor(154)
    2
    """
    return next(gen_prime_factors(n))


def largest_prime_factor(n):
    """Returns the largest prime factor of n
    n: An int >= 2
    Raises a ValueError if n < 2
    >>> largest_prime_factor(77)
    11
    >>> largest_prime_factor(7 * 17)
    17
    """
    return max(gen_prime_factors(n))


def modinv(x, n):
    """
      16  23
       0   1  = 23
       1   0  = 16
      -1   1  =  7
       3  -2  =  2
     -10   7  =  1
      23 -16  =  0
      13  -9  =  1

    >>> modinv(9, 13)
    3
    >>> modinv(13, 9)
    7
    >>> modinv(5, 8)
    5
    >>> modinv(6, 8)
    0
    """
    a, m, b, k = n, 0, x, 1
    while b > 0:
        q, r = divmod(a, b)
        a, m, b, k = b, k, r, m - q * k
    return 0 if a > 1 else m if m > 0 else n + m


if __name__ == "__main__":
    # print([(x, modinv(x, 23)) for x in range(1, 23)])
    print(divisors(2**3 * 3**2 * 5 * 7))
