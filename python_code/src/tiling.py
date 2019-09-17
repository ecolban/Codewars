M = 12345787


def three_by_even_n(n):
    a_even, c_even = 1, 0
    for _ in range(n // 2):
        a_even, c_even = (3 * a_even + 2 * c_even) % M, (a_even + c_even) % M
    return a_even


def three_by_n(n):
    a_even, b_even, c_even, a_odd, b_odd, c_odd, a_prev = 1, 0, 0, 0, 0, 0, 0
    for i in range(n):
        a_even, b_even, c_even, a_odd, b_odd, c_odd, a_prev = \
            (2 * b_odd + a_prev) % M, \
            (a_odd + b_odd + c_odd) % M, \
            b_odd % M, \
            (2 * a_even + 2 * b_even + 2 * c_even + a_prev) % M, \
            (a_even + c_even) % M, \
            (a_even + b_even) % M, \
            a_even if i % 2 == 0 else a_odd
    return a_even if n % 2 == 0 else a_odd


def five_by_2n(n):
    """
    Google "8, 95, 1183 oeis" and you get immediately that this is the beginning
    of A003775 (Number of perfect matchings (or domino tilings) in P_5 X P_2n).
    Moreover: b(n) = 15b(n-1) - 32b(n-2) + 15b(n-3) - b(n-4)"""
    n_4, n_3, n_2, n_1 = 1, 8, 5, 3
    for _ in range(n):
        n_4, n_3, n_2, n_1 = n_3, n_2, n_1, (15 * n_1 - 32 * n_2 + 15 * n_3 - n_4) % M
    return n_4


if __name__ == "__main__":
    for i in range(1, 10):
        print(five_by_2n(i), end=", ")
