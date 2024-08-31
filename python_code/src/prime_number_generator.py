from time import perf_counter

from prime_factorization import is_prime

GAPS = (
    2, 1, 2, 3, 1, 3, 2, 1, 2, 3, 3, 1, 3, 2, 1, 3, 2, 3, 4, 2, 1, 2, 1, 2, 7, 2, 3, 1, 5, 1, 3, 3, 2, 1, 2, 3,
    1, 5, 1, 2, 1, 6, 5, 1, 2, 1, 2, 3, 1, 3, 2, 3, 3, 3, 1, 3, 2, 1, 3, 2, 3, 4, 2, 1, 2, 3, 4, 3, 5, 1, 2, 3,
    1, 3, 3, 2, 1, 2, 3, 1, 3, 2, 1, 3, 5, 1, 5, 1, 2, 1, 2, 3, 4, 2, 1, 2, 6, 1, 3, 2, 1, 3, 2, 3, 6, 1, 2, 1,
    2, 4, 3, 2, 3, 1, 2, 3, 1, 3, 5, 1, 2, 3, 1, 3, 2, 1, 2, 1, 5, 1, 5, 1, 2, 3, 3, 1, 3, 3, 2, 3, 3, 1, 3, 2,
    1, 3, 2, 3, 4, 2, 1, 3, 2, 4, 3, 2, 3, 1, 2, 3, 4, 3, 2, 1, 5, 1, 3, 2, 1, 2, 1, 5, 1, 5, 1, 2, 1, 2, 4, 3,
    2, 1, 2, 3, 3, 1, 3, 2, 4, 2, 3, 4, 2, 1, 2, 1, 2, 4, 3, 2, 3, 3, 3, 1, 3, 3, 2, 1, 2, 3, 1, 3, 2, 1, 2, 1,
    5, 1, 5, 1, 3, 2, 3, 1, 3, 2, 1, 2, 3, 3, 4, 2, 1, 3, 5, 4, 2, 1, 2, 1, 2, 4, 5, 3, 1, 2, 4, 3, 3, 2, 1, 2,
    3, 1, 3, 2, 3, 1, 5, 1, 5, 1, 2, 1, 2, 3, 1, 3, 2, 1, 2, 3, 3, 1, 3, 3, 3, 2, 3, 4, 2, 1, 2, 1, 2, 4, 3, 2,
    4, 2, 3, 1, 3, 3, 2, 1, 2, 3, 4, 2, 1, 2, 1, 5, 1, 5, 1, 2, 1, 2, 3, 1, 5, 1, 2, 3, 4, 3, 2, 1, 3, 2, 3, 4,
    2, 3, 1, 2, 4, 3, 2, 3, 1, 2, 3, 1, 3, 3, 2, 3, 3, 1, 3, 3, 2, 1, 5, 1, 5, 1, 2, 1, 2, 3, 1, 3, 2, 1, 5, 3,
    1, 3, 2, 1, 3, 2, 3, 4, 2, 1, 2, 1, 6, 3, 2, 3, 1, 2, 3, 1, 6, 2, 1, 2, 4, 3, 2, 1, 2, 1, 5, 1, 5, 3, 1, 2,
    3, 1, 3, 2, 1, 2, 3, 3, 1, 3, 2, 1, 5, 3, 4, 3, 2, 1, 2, 4, 3, 2, 3, 1, 2, 3, 1, 3, 3, 3, 2, 3, 1, 3, 2, 1,
    2, 1, 5, 6, 1, 2, 1, 5, 1, 3, 2, 1, 2, 3, 3, 1, 5, 1, 3, 2, 7, 2, 1, 2, 1, 2, 4, 3, 2, 3, 1, 2, 3, 1, 3, 3,
    2, 1, 2, 3, 1, 3, 2, 1, 2, 6, 1, 6
)


class Wheel:

    def __init__(self, start=0, idx=0):
        self._current = start  # the next value to yield
        self._idx = idx  # the index to the next value to yield

    def __iter__(self):
        return self

    def __next__(self):
        res = self._current
        self._current += GAPS[self._idx]
        self._idx = (self._idx + 1) % len(GAPS)
        return res

    def copy(self):
        return Wheel(start=self._current, idx=self._idx)


class Primes:
    WHEEL = Wheel()
    SIEVE = [False] * 16_000_000
    while (i := next(WHEEL)) < len(SIEVE):
        SIEVE[i] = True
    LAST = (0, 0)

    @staticmethod
    def stream():
        if Primes.LAST == (0, 0):
            yield from (2, 3, 5, 7, 11)
            wheel = Wheel()
        else:
            idx, start = Primes.LAST
            wheel = Wheel(start=start, idx=idx)
            next(wheel)
        for i, n in enumerate(wheel):
            if n >= len(Primes.SIEVE):
                break
            t = Primes.SIEVE[n]
            p = 13 + 2 * n
            if t:
                yield p
                Primes.LAST = (wheel._idx, wheel._current)
                ii_ = (p * p - 13) // 2
                if ii_ < len(Primes.SIEVE):
                    Primes.SIEVE[ii_] = False
                for i_ in wheel.copy():
                    p_ = 13 + 2 * i_
                    ii_ = (p * p_ - 13) // 2
                    if ii_ >= len(Primes.SIEVE):
                        break
                    Primes.SIEVE[ii_] = False


if __name__ == '__main__':
    start = perf_counter()
    g = Primes.stream()
    for _ in range(999_999):
        next(g)
    print(next(g))
    print(f"Time = {perf_counter() - start:.2f} s")
