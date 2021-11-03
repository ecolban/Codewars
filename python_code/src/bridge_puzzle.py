from functools import cache
from itertools import combinations

from prime_factorization import is_prime


def root(n):
    return int(n ** 0.5)


@cache
def statement1(n):
    return n % 2 == 1 and not is_prime(n - 2)


@cache
def statement2(n):
    return sum(statement1(k + n // k) for k in range(2, root(n) + 1) if n % k == 0) == 1


def statement3(n):
    return sum(statement2(k * (n - k)) for k in range(2, n // 2 + 1)) == 1


def is_solution(a, b):
    return statement1(a + b) and statement2(a * b) and statement3(a + b)


if __name__ == '__main__':
    solutions = ((a, b) for a, b in combinations(range(2, 1000), 2) if is_solution(a, b))
    print([(a, b) for a, b in solutions for p, q in ((a, b) if a % 2 == 0 else (b, a),)
           if not is_prime(q) and p not in (2, 4, 8, 16, 32, 64, 128, 256, 512)])
