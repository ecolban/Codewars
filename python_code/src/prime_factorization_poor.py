
# def prime_factors(n):
#     """Return a list of prime numbers that divide n in ascending order. For example,
#     prime_factors(12) returns [2, 2, 3]."""
#     res = []
#     factor = 2
#     while factor * factor <= n:
#         if n % factor == 0:
#             res.append(factor)
#             n //= factor
#         else:
#             factor = factor + (1 if factor == 2 else 2)
#     if n > 1:
#         res.append(n)
#     return res


def prime_factors(n):
    """Return a list of pairs in ascending order, where each pair
    consists of a prime factor of n and the number of times that
    that prome factor divides n. For example, prime_factors(12)
    returns [(2, 2), (3, 1)]."""
    res = []
    factor = 2
    while factor * factor <= n:
        if n % factor == 0:
            factor_count = 0
            while n % factor == 0:
                factor_count += 1
                n //= factor
            res.append((factor, factor_count))
        factor = factor + (1 if factor == 2 else 2)
    if n > 1:
        res.append((n, 1))
    return res


def is_prime(n):
    factor = 2
    while factor * factor <= n:
        if n % factor == 0:
            return False
        factor = factor + (2 if factor >= 3 else 1)
    return True


def totient(n):
    res = n
    factor = 2
    while factor * factor <= n:
        if n % factor == 0:
            n //= factor
            res -= res // factor
            while n % factor == 0:
                n //= factor
        factor = factor + (2 if factor >= 3 else 1)
    if n > 1:
        res -= res // n
    return res


def smallest_prime_factor(n):
    """Returns the smallest prime factor of n
    n: An int >= 2
    Raises a StopIteration if n < 2
    """
    if n < 2:
        raise StopIteration
    factor = 2
    while factor * factor <= n:
        if n % factor == 0:
            return factor
        factor = factor + (2 if factor >= 3 else 1)
    return n


def largest_prime_factor(n):
    """Returns the largest prime factor of n
    n: An int >= 2
    Raises a ValueError if n < 2
    """
    if n < 2:
        raise ValueError
    factor = 2
    while factor * factor <= n:
        if n % factor == 0:
            n //= factor
        else:
            factor = factor + (1 if factor == 2 else 2)
    return n if n > 1 else factor
