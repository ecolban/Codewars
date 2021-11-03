from collections import deque
from string import ascii_lowercase

MOVES = [(i, j) for i in (-2, -1, 1, 2) for j in (-3 + abs(i), 3 - abs(i))]
NUM_ROWS = 8
NUM_COLS = 8

DISTS = [
    [0, 3, 2, 3, 2, 3, 4, 5, ],
    [3, 4, 1, 2, 3, 4, 3, 4, ],
    [2, 1, 4, 3, 2, 3, 4, 5, ],
    [3, 2, 3, 2, 3, 4, 3, 4, ],
    [2, 3, 2, 3, 4, 3, 4, 5, ],
    [3, 4, 3, 4, 3, 4, 5, 4, ],
    [4, 3, 4, 3, 4, 5, 4, 5, ],
    [5, 4, 5, 4, 5, 4, 5, 6, ],
]


def neighbors(pos):
    row, col = pos
    for i, j in MOVES:
        if 0 <= row + i < NUM_ROWS and 0 <= col + j < NUM_COLS:
            yield row + i, col + j


def knight(p1, p2):
    start = int(p1[1:]) - 1, ascii_lowercase[:NUM_COLS].index(p1[0])
    end = int(p2[1:]) - 1, ascii_lowercase[:NUM_COLS].index(p2[0])
    return knight_(start, end)


def knight_(start, end):
    if start == end: return 0
    h, seen, pos, d = deque(), {start}, start, 0
    while True:
        for n in neighbors(pos):
            if n == end: return d + 1
            if n not in seen:
                seen.add(n)
                h.append((d + 1, n))
        d, pos = h.popleft()


if __name__ == '__main__':
    start = (0, 0)
    for r in range(NUM_ROWS):
        print(*(k if (k := knight_(start, (r, c))) < 8 else '.'
                for c in range(NUM_COLS)), sep=', ')
