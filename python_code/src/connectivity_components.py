from collections import Counter
from textwrap import dedent


def components(grid):
    rs = grid.split('\n')
    cols = rs[0].count('+') - 1
    rows = len(rs) // 2
    cells = [r * cols + c for r in range(rows) for c in range(cols)]

    def union(c1, c2):
        c1 = find(c1)
        c2 = find(c2)
        if c1 != c2:
            cells[c1] = c2

    def find(c):
        if cells[c] == c:
            return c
        root = find(cells[c])
        cells[c] = root
        return root

    def no_wall_on_right(r, c):
        return rs[2 * r + 1][3 * c + 3] == ' '

    def no_wall_below(r, c):
        return rs[2 * (r + 1)][3 * c + 1: 3 * c + 3] == '  '

    for r in range(rows):
        for c in range(cols):
            cell_idx = r * cols + c
            if no_wall_on_right(r, c):
                union(cell_idx, cell_idx + 1)
            if no_wall_below(r, c):
                union(cell_idx, cell_idx + cols)

    for r in range(rows):
        for c in range(cols):
            cells[r * cols + c] = find(r * cols + c)

    return sorted(Counter(Counter(cells).values()).items(), reverse=True)


def test_connecticity_components():
    assert components(
        dedent('''
            +--+--+--+
            |  |     |
            +  +  +--+
            |  |  |  |
            +--+--+--+
        ''').strip()) == [(3, 1), (2, 1), (1, 1)]
    assert components(
        dedent('''
            +--+--+--+
            |  |     |
            +  +  +--+
            |        |
            +--+--+--+'
            ''').strip()) == [(6, 1)]
    assert components(
        dedent('''
            +--+--+--+
            |  |  |  |
            +--+--+--+
            |  |  |  |
            +--+--+--+
            ''').strip()) == [(1, 6)]
    assert components(
        dedent('''
            +--+--+--+--+--+
            |        |  |  |
            +  +--+  +  +  +
            |     |  |     |
            +--+--+  +--+--+
            |  |  |        |
            +--+--+--+--+--+
            ''').strip()) == [(9, 1), (4, 1), (1, 2)]
