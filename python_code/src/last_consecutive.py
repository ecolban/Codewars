import time


def last_consecutive_old(a):
    a, prev = iter(a), None

    def next_consecutive():
        n = next(a, None)
        return n if prev is None or prev + 1 == n else None

    for m in iter(next_consecutive, None):
        prev = m
    return prev


def last_consecutive(a):
    a, prev = iter(a), None
    for n in a:
        if prev is not None and prev + 1 != n:
            break
        else:
            prev = n
    return prev


if __name__ == '__main__':
    start = time.time()
    assert last_consecutive([]) is None
    assert last_consecutive([1]) == 1
    assert last_consecutive([1, 2, 4]) == 2
    assert last_consecutive([1, 2, 3]) == 3
    assert last_consecutive((n for n in range(1, 1 << 100) if n != 3)) == 2
    assert last_consecutive(n if n < 10 else 10 for n in range(1, 1 << 100)) == 10
    print(f'Time = {(time.time() - start) * 1000:.3f} ms')
