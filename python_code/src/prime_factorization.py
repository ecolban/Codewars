import asyncio
import time
from collections import Counter
from functools import reduce
from itertools import chain, count, cycle, groupby, product
from math import gcd
from operator import mul
from random import randrange



def gen_prime_factors(n):
    """Generate all the prime factors of n in ascending order"""
    gaps = chain((1, 2, 2,), cycle((4, 2, 4, 2, 4, 6, 2, 6,)))
    factor = 2
    while factor * factor <= n:
        if n % factor == 0:
            yield factor
            n //= factor
        else:
            factor += next(gaps)
    if n > 1:
        yield n


def make_gaps(n):
    if n == 0:
        yield from chain((1,), cycle((2,)))
    gaps = make_gaps(n - 1)
    k, p = 0, 2
    for i in range(n):
        k = next(gaps)
        p += k
        yield k
    m = 0
    while True:
        k = next(gaps)
        if (m + k) % p == 0:
            k += next(gaps)
        m = (m + k) % p
        yield k


def make_gaps_2(n):
    if n == 0:
        return (1,), (2,)
    prefix_in, loop_in = make_gaps_2(n - 1)
    loop_iter = cycle(loop_in)
    p = 2 + sum(prefix_in)
    k = next(loop_iter)
    prefix_out = (*prefix_in, k)

    def loop_out_gen(k):
        m = k
        for _ in range(len(loop_in) * (p - 1)):
            k = next(loop_iter)
            m = (m + k) % p
            if m == 0:
                m = next(loop_iter)
                k += m
            yield k

    return prefix_out, tuple(loop_out_gen(k))


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


def tower(base, h, m):
    """Return base ** base ** ... ** base, where the height is h, modulo m. """
    if m == 1: return 0
    if base == 1 or h == 0: return 1
    i, exponent = 0, 1
    while exponent < m and i < h - 1:
        i += 1
        exponent = pow(base, exponent)
    if i == h - 1:
        return pow(base, exponent, m)
    t = totient(m)
    return pow(base, tower(base, h - 1, t) + t, m)


def generate_keys():
    p = sympy.randprime(1 << 999, 1 << 1000)
    q = sympy.randprime(1 << 999, 1 << 1000)
    n = p * q
    phi = n - p - q + 1
    candidates = (randrange(3, phi, 2) for _ in count())
    k1 = next(k for k in candidates if gcd(k, phi) == 1)
    k2 = sympy.mod_inverse(k1, phi)
    return k1, k2, n


def encrypt(message, k1, n):
    return pow(message, k1, n)


def decrypt(message, k2, n):
    return pow(message, k2, n)


def public_key_example():
    k1, k2, n = generate_keys()
    print(f'length of n = {len(str(n))}', f'k1 = {k1}', f'k2 = {k2}', f'n  = {n}', sep='\n')
    for _ in range(1):
        message = randrange(1, n)
        encrypted = encrypt(message, k1, n)
        decrypted = decrypt(encrypted, k2, n)
        assert message == decrypted, "Failure!"
        print(f'\nmessage   = {message}'
              f'\nencrypted = {encrypted}'
              f'\ndecrypted = {decrypted}')


def multi_threading_example():
    my_list = []
    asyncio.run(extend_list(my_list))
    print(len(my_list))
    print(Counter(zip(my_list, my_list[1:], my_list[2:])))


async def extend_list(a_list):
    statements = [my_list_update(a_list, c) for c in 'ab']
    await asyncio.gather(*statements)


async def my_list_update(a_list, c):
    def run():
        for _ in range(25):
            time.sleep(0.000000001)
            a_list.extend([c, c])

    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, run)


def count_prime_divisors(n):
    return sum(1 for _ in gen_prime_factors(n))


def count_k_primes(k, start, end):
    return [i for i in range(start, end) if count_prime_divisors(i) == k]


def puzzle(s):
    return sum(a + b + c == s
               for a in count_k_primes(7, 2, s - 9)
               for b in count_k_primes(3, 2, s - a - 1)
               for c in count_k_primes(1, 2, s - a - b + 1))


def consec_kprimes(k, arr):
    idx = [i for i, n in enumerate(arr) if count_prime_divisors(n) == k]
    return sum(i + 1 == j for i, j in zip(idx, idx[1:]))


if __name__ == "__main__":
    multi_threading_example()
    print(count_k_primes(5, 1000, 1100))
    print(puzzle(143))
    g = make_gaps(1)
    print(*(next(g) for _ in range(10)))
