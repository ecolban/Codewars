from math import ceil
from string import ascii_lowercase


def char_gen(s, shift, forward=True):
    for c in s:
        n = ascii_lowercase.find(c.lower())
        if n == -1:
            yield c
        else:
            c_out = ascii_lowercase[(n + shift) % 26]
            yield c_out.upper() if c.isupper() else c_out
        shift = shift + (1 if forward else -1)


def parts(a, k):
    n = len(a)
    start = 0
    p = ceil(n / k)
    for i in range(k):
        p = min(n, p)
        yield ''.join(a[start: start + p])
        start += p
        n -= p


def moving_shift(s, shift):
    res = list(parts(list(char_gen(s, shift)), 5))
    return res


def demoving_shift(parts, shift):
    s = ''.join(parts)
    return ''.join(char_gen(s, -shift, forward=False))


if __name__ == '__main__':
    for (s, shift), expected in [
        (("How can we become the kind of people that face our fear and do it anyway?", 1),
         ["Iqz hgu fo nrqd", "cv mbz hgmd qi ", "ukvxuo fuoi wsv", "y krp ffcu ftk ", "my ug pdpots?"]),
        (("I should have known that you would have a perfect answer for me!!!", 1),
         ["J vltasl rlhr ", "zdfog odxr ypw", " atasl rlhr p ", "gwkzzyq zntyhv", " lvz wp!!!"])
    ]:
        actual = moving_shift(s, shift)
        print(actual)
        print([len(p) for p in actual])
        print([len(p) for p in expected])
        assert actual == expected
        back = demoving_shift(actual, shift)
        print(back)
        assert back == s
