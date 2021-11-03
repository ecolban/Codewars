import time
from random import randrange


class ShrinkList:

    def __init__(self, a):
        n = len(a)
        self._a = a.copy()
        self._len = n
        self.index_tree = make_index_tree(n)
        self.adjust = [0] * n

    def __getitem__(self, i):
        return self._a[self._map_index(i)]

    def __setitem__(self, i, value):
        self._a[self._map_index(i)] = value

    def __len__(self):
        return self._len

    def _map_index(self, i):
        def h(j, p):
            r = self.index_tree[p]
            if j + self.adjust[p] < r:
                res = h(j, 2 * p + 1)
            elif self._a[r] is None:
                res = h(j + self.adjust[p] + 1, 2 * p + 2)
            elif j + self.adjust[p] == r:
                res = j + self.adjust[p]
            else:
                res = h(j + self.adjust[p], 2 * p + 2)
            return res

        return h(i, 0)

    def pop(self, i):
        def h(j, p):
            r = self.index_tree[p]
            if j + self.adjust[p] < r:
                res = h(j, 2 * p + 1)
                self.adjust[p] += 1
            elif self._a[r] is None:
                res = h(j + self.adjust[p] + 1, 2 * p + 2)
            elif j + self.adjust[p] == r:
                res = self._a[r]
                self._a[r] = None
            else:
                res = h(j + self.adjust[p], 2 * p + 2)
            return res

        return_value = h(i, 0)
        self._len -= 1
        return return_value

    def __str__(self):
        return str([e for e in self._a if e is not None])


def make_index_tree(n):
    it = iter(range(n))
    res = [0] * n

    def h(k):
        if k >= n: return
        h(2 * k + 1)
        res[k] = next(it)
        h(2 * k + 2)

    h(0)
    return res


if __name__ == '__main__':
    N = 512 * 1024
    a = [randrange(1, 101) for _ in range(N)]
    # a.sort()
    b = a.copy()
    pops = [i - 1 for i in range(N, N // 2, -1)]
    start = time.time()
    sl = ShrinkList(a)
    for i in pops:
        sl.pop(i)
    print([sl[i] for i in range(20)])
    print(time.time() - start)
    start = time.time()
    for i in pops:
        b.pop(i)
    print([b[i] for i in range(20)])
    print(time.time() - start)
