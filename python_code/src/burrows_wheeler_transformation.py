import time


def encode(s):
    n = len(s)
    a = sorted(range(n), key=lambda i: s[i:] + s[:i])
    return ''.join(s[(i - 1) % n] for i in a), a.index(0)


def decode(s, start):
    ls = sorted((c, i) for i, c in enumerate(s))

    def h(i):
        for _ in range(len(s)):
            c, i = ls[i]
            yield c

    return ''.join(h(start))


if __name__ == '__main__':
    start_time = time.time()
    encoded, i = encode('bananabar')
    ls = [(c, i) for i, c in enumerate(encoded)]
    print(ls)
    print(sorted(ls))
    print(encoded, i)
    print(decode(encoded, i))
