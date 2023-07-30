from random import randrange


def or_sum(n: int, k: int) -> int:
    p = 1
    res = n if k & 1 else (n + 1) // 2
    while p < max(n, k):
        p <<= 1
        if p & k:
            res += p * n
        else:
            q, r = divmod(n, p)
            res += q // 2 * p * p
            if q % 2 == 1:
                res += (r + 1) * p
    return res


def or_sum_slow(n: int, k: int) -> int:
    return sum(i | k for i in range(1, n + 1))


def bit_count(n, p):
    q, r = divmod(n + 1, p << 1)
    return q * p + max(0, r - p)


def sxore(n):
    return (n,1,n+1,0)[n%4]


if __name__ == '__main__':
    print(or_sum(1_000_000_000, 2_989_093))
    # print(or_sum_slow(1_000_000_000, 2_989_093))
    print(bit_count(2, 2))
    print(sxore(2))
