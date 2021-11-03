from collections import deque
from heapq import heappop, heappush

import numpy as np


def dbl_linear1(m):
    seq = [1]
    prev = None
    i, n = 0, 0
    while i <= m:
        n = heappop(seq)
        if n == prev: continue
        prev = n
        heappush(seq, 2 * n + 1)
        heappush(seq, 3 * n + 1)
        i += 1
    return n


def dbl_linear2(m):
    seq = np.array([0] * (m + 2))
    i2 = i3 = 0
    v2 = v3 = 1
    for i in range(1, m + 2):
        cond = v3 <= v2
        if v2 <= v3:
            seq[i] = v2
            i2 += 1
            v2 = 2 * seq[i2] + 1
        if cond:
            seq[i] = v3
            i3 += 1
            v3 = 3 * seq[i3] + 1
        assert i3 <= i2
    return seq[m + 1]

def dbl_linear3(m):
    seq = deque([0])
    i2 = 0
    v2 = v3 = 1
    for i in range(1, m + 2):
        if v2 < v3:
            seq.append(v2)
            i2 += 1
            v2 = 2 * seq[i2] + 1
        else:
            seq.append(v3)
            seq.popleft()
            if v2 == v3:
                v2 = 2 * seq[i2] + 1
            else:
                i2 -= 1
            v3 = 3 * seq[0] + 1
    return seq[-1]


if __name__ == '__main__':
    print(dbl_linear1(500000))
    print(dbl_linear2(500000))
    print(dbl_linear3(500000))
