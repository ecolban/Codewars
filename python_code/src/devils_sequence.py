from math import log, floor


def count_sixes(n):
    d = 3 << (n - 1)
    j = floor(log(d, 10)) - 1
    p = d // 10 ** j
    adj = 1 if p >= (15 + n % 2 * 15) else 0
    return j + adj


def alt(n):
    return floor((n - n % 2) * log(2, 10))


if __name__ == "__main__":
    print(next((n for n in range(100000, 120000) if count_sixes(n) != alt(n)), None))
