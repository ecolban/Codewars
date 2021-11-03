from fractions import Fraction

from prime_factorization import prime_factors


def gcd_round(a, b, epsilon):
    if b == 0:
        return a
    while abs(a / b) > epsilon:
        a, b = b % a, a
    return b


def decimal(numerator, denominator, base=10):
    memo = {}
    res = []
    for i in range(denominator):
        quotient, numerator = divmod(numerator, denominator)
        res.append(quotient)
        numerator *= base
        if numerator == 0 or numerator in memo:
            break
        memo[numerator] = i + 1
    return res, memo[numerator] if numerator else None


def expand(n, base=10):
    memo = {}
    res = []
    numerator = 1
    for i in range(n):
        numerator *= base
        if numerator == 0 or numerator in memo:
            break
        memo[numerator] = i
        quotient, numerator = divmod(numerator, n)
        res.append(quotient)
    return res, memo[numerator] if numerator else None


def period_len(n, d, base=10):
    f, p = decimal(n, d, base)
    return len(f) - (p if p else 1)


if __name__ == "__main__":
    f = Fraction(0.1)
    # print(len(decimal(f.numerator, f.denominator, 5)))
    print(prime_factors(f.numerator))
    print(prime_factors(f.denominator))
    print(decimal(f.numerator, f.denominator, 16))
    print(expand(10, 16))
    print(decimal(1, 10, 5))
    print(expand(10, 5))
    print(decimal(1, 97))
    a = expand(97)
    print(a)
    b = int(''.join(str(i) for i in a[0]))
    print(b)
    print(97 * b)
    print(len(str(97 * b)))
    print(expand(10, 10))
