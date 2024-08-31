from collections.abc import Generator


def roman_fractions(n: int, f: int = 0) -> str:
    if not (0 <= n <= 5000 and 0 <= f < 12):
        return "NaR"
    if n == 0 and f == 0:
        return 'N'
    return ''.join(gen_roman(n, f))


def gen_roman(n: int, f: int) -> Generator[str]:
    def digit_to_roman(unit: int, one: str, five: str, ten: str) -> Generator[str]:
        assert unit <= n < 10 * unit
        q, r = divmod(n, unit)
        if q == 9:
            yield one + ten
        elif 5 <= q:
            yield five + one * (q - 5)
        elif q == 4:
            yield one + five
        else:
            yield one * q
        return r

    if n >= 1000:
        q_, n = divmod(n, 1000)
        yield 'M' * q_
    if n >= 100:
        n = yield from digit_to_roman(100, *'CDM')
    if n >= 10:
        n = yield from digit_to_roman(10, *'XLC')
    if n >= 1:
        n = yield from digit_to_roman(1, *'IVX')
    if f > 0:
        yield ('', '.', ':', ':.', '::', ':.:', 'S', 'S.', 'S:', 'S:.', 'S::', 'S:.:')[f]


if __name__ == '__main__':
    print(roman_fractions(1001))
    print(roman_fractions(2024))
    print(roman_fractions(1637))
    print(roman_fractions(1981))
    print(roman_fractions(5000, 7))
    print(roman_fractions(0, 7))
    print(roman_fractions(0))
