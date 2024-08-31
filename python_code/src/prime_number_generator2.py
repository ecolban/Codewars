from itertools import *
from time import perf_counter

from prime_factorization import is_prime


class Primes:

    @staticmethod
    def wsieve():  # wheel-sieve, by Will Ness.   ideone.com/trR9OI
        yield 11  # cf. ideone.com/WFv4f
        mults = {}  # codereview.stackexchange.com/q/92365/9064
        ps = Primes.wsieve()
        p = next(ps)  # 11
        psq = p * p  # 121
        D = dict(zip(
            accumulate([
                0,  # where to start
                2, 4, 2, 4, 6, 2, 6, 4, 2, 4, 6, 6, 2, 6, 4, 2, 6, 4, 6, 8, 4, 2, 4, 2,
                4, 8, 6, 4, 6, 2, 4, 6, 2, 6, 6, 4, 2, 4, 6, 2, 6, 4, 2, 4, 2, 10, 2, 10,
            ]),
            count(0),
        ))
        for c in accumulate(chain([13], cycle(
                [4, 2, 4, 6, 2, 6, 4, 2, 4, 6, 6, 2, 6, 4, 2, 6, 4, 6, 8, 4, 2, 4, 2,
                 4, 8, 6, 4, 6, 2, 4, 6, 2, 6, 6, 4, 2, 4, 6, 2, 6, 4, 2, 4, 2, 10, 2, 10, 2]))):
            if c in mults:
                wheel = mults.pop(c)
            elif c < psq:
                yield c
                continue
            else:  # (c==psq)
                p2 = p * 2
                p6 = p * 6
                p10 = p * 10  # map (p*) (roll wh from p) =
                p4 = p * 4
                p8 = p * 8  # = roll (wh*p) from p*p
                wheel = accumulate(chain(
                    [p * p],
                    islice(
                        cycle([
                            p2, p4, p2, p4, p6, p2, p6, p4, p2, p4, p6, p6,
                            p2, p6, p4, p2, p6, p4, p6, p8, p4, p2, p4, p2,
                            p4, p8, p6, p4, p6, p2, p4, p6, p2, p6, p6, p4,
                            p2, p4, p6, p2, p6, p4, p2, p4, p2, p10, p2, p10
                        ]),
                        D[(p - 11) % 210],
                        None
                    )
                ))
                p = next(ps)
                psq = p * p
                next(wheel)  # p*p
            # for m in wheel:
            #     if m not in mults:
            #         break
            while (m := next(wheel)) in mults:
                pass
            # m = next(k for k in wheel if k not in mults)
            mults[m] = wheel

    @staticmethod
    def stream():
        yield from (2, 3, 5, 7)
        yield from Primes.wsieve()


def test_wsieve():
    start = perf_counter()
    g = Primes.stream()
    for _ in range(999_999):
        next(g)
    p = next(g)
    assert is_prime(p)
    print(p)
    print(f"Time = {perf_counter() - start:.2f} s")
    # print(dict(zip(
    #         accumulate([
    #             0,  # where to start
    #             2, 4, 2, 4, 6, 2, 6, 4, 2, 4, 6, 6, 2, 6, 4, 2, 6, 4, 6, 8, 4, 2, 4, 2,
    #             4, 8, 6, 4, 6, 2, 4, 6, 2, 6, 6, 4, 2, 4, 6, 2, 6, 4, 2, 4, 2, 10, 2, 10,
    #         ]),
    #         count(0),
    #     )))
