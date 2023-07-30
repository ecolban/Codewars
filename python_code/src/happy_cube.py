import csv
from enum import Enum
from functools import reduce
from itertools import groupby, combinations, count
from operator import or_
from random import shuffle
from time import time
from typing import Optional, Iterable

N, E, S, W = 0, 1, 2, 3


class Pads(Enum):
    BLUE = """
    01000
    01111
    11111
    01110
    00100

    00100
    11111
    01110
    11111
    01010

    11011
    01111
    01110
    11110
    10100

    10101
    11111
    01110
    11110
    11011

    01010
    11110
    01111
    11111
    00100
    
    10100
    11111
    11111
    01110
    00100
    """

    GREEN = """
    11010
    01110
    11111
    01110
    01010

    01011
    11110
    01111
    11110
    01010

    11011
    01110
    11111
    01110
    01010

    01011
    01111
    11110
    01111
    11010

    00100
    01110
    11111
    01110
    00100

    00100
    01111
    11110
    01111
    11011
    """

    PINK = """
    00100
    11111
    01110
    11111
    01010

    01100
    01111
    11110
    01111
    00100

    00011
    11110
    01111
    11110
    00100

    10101
    11111
    01110
    11111
    11000

    00100
    01110
    11111
    11110
    10100

    11011
    11111
    01110
    11111
    10100    
    """

    PURPLE = """
    11000
    11111
    01110
    01111
    01010

    10101
    11111
    01110
    01110
    01100

    00111
    11111
    11110
    01110
    01010

    00100
    01111
    11111
    11110
    10100

    11001
    01111
    11110
    01111
    01010

    10100
    11110
    01111
    01111
    01100
    """

    RED = """
    11101
    01111
    11110
    01110
    00100

    01000
    11111
    01111
    11110
    01010

    01011
    01111
    11110
    01110
    01010

    10101
    11111
    01111
    11110
    11010

    00101
    01111
    11111
    11110
    00100

    00100
    01111
    01110
    11110
    11010
    """

    YELLOW = """
    11011
    01111
    11110
    01111
    00011

    00110
    01110
    11111
    01110
    01010

    00100
    11110
    01110
    11111
    00111

    11000
    11111
    01110
    01111
    11011

    00100
    11110
    01111
    11111
    11000

    00100
    11110
    11111
    01110
    01100
    """

    def to_list(self):
        v = self.value.strip('\n')
        lines = v.split('\n')
        return '\n'.join(line.lstrip(' ') for line in lines).split('\n\n')


#  0
# 123
#  4
#  5
PROBLEM1 = {
    0: ((5, S), (3, N), (2, N), (1, N)),
    1: ((0, W), (2, W), (4, W), (5, W)),
    2: ((0, S), (3, W), (4, N), (1, E)),
    3: ((0, E), (5, E), (4, E), (2, E)),
    4: ((2, S), (3, S), (5, N), (1, S)),
    5: ((4, S), (3, E), (0, N), (1, W)),
}
# N, E, S, W = 0, 1, 2, 3
#  01
# 2345
#  67
#  89
PROBLEM2 = {
    0: ((8, S), (1, W), (3, N), (2, N)),
    1: ((9, S), (5, N), (4, N), (0, E)),
    2: ((0, W), (3, W), (6, W), (8, W)),
    3: ((0, S), (4, W), (6, N), (2, E)),
    4: ((1, S), (5, W), (7, N), (3, E)),
    5: ((1, E), (9, E), (7, E), (4, E)),
    6: ((3, S), (7, W), (8, N), (2, S)),
    7: ((4, S), (5, S), (9, N), (6, E)),
    8: ((6, S), (9, W), (0, N), (2, W)),
    9: ((7, S), (5, E), (1, N), (8, E)),
}
# N, E, S, W = 0, 1, 2, 3
#  012
# 34567
#  89A
#  BCD
PROBLEM3 = {
    0: ((11, S), (1, W), (4, N), (3, N)),
    1: ((12, S), (2, W), (5, N), (0, E)),
    2: ((17, S), (7, N), (6, N), (1, E)),
    3: ((0, W), (4, W), (8, W), (11, W)),
    4: ((0, S), (5, W), (8, N), (3, E)),
    5: ((1, S), (6, W), (9, N), (4, E)),
    6: ((2, S), (7, W), (10, N), (5, E)),
    7: ((2, E), (16, E), (10, E), (6, E)),
    8: ((4, S), (9, W), (11, N), (3, S)),
    9: ((5, S), (10, W), (12, N), (8, E)),
    10: ((6, S), (7, S), (13, N), (9, E)),
    11: ((8, S), (12, W), (0, N), (3, W)),
    12: ((9, S), (14, W), (1, N), (11, E)),
    # 13: ((10, S), (7, E), (2, N), (12, E)),
    13: ((10, S), (16, N), (15, N), (14, N)),
    14: ((13, W), (15, W), (17, W), (12, E)),
    15: ((13, S), (16, W), (17, N), (14, E)),
    16: ((13, E), (7, E), (17, E), (15, E)),
    17: ((15, S), (16, S), (2, N), (14, S)),
}
#   01
#   23
# 456789
# abcdef
#   gh
#   ij
#   kl
#   mn
PROBLEM4 = {
    0: ((22, S), (1, W), (2, N), (4, N)),
    1: ((23, S), (9, N), (3, N), (0, E)),
    2: ((0, S), (3, W), (6, N), (5, N)),
    3: ((1, S), (8, N), (7, N), (2, E)),
    4: ((0, W), (5, W), (10, N), (22, W)),
    5: ((2, W), (6, W), (11, N), (4, E)),
    6: ((2, S), (7, W), (12, N), (5, E)),
    7: ((3, S), (8, W), (13, N), (6, E)),
    8: ((3, E), (9, W), (14, N), (7, E)),
    9: ((1, E), (23, E), (15, N), (8, E)),
    10: ((4, S), (11, W), (18, W), (20, W)),  # a
    11: ((5, S), (12, W), (16, W), (10, E)),  # b
    12: ((6, S), (13, W), (16, N), (11, E)),  # c
    13: ((7, S), (14, W), (17, N), (12, E)),  # d
    14: ((8, S), (15, W), (17, E), (13, E)),  # e
    15: ((9, S), (21, E), (19, E), (14, E)),  # f
    16: ((12, S), (17, W), (18, N), (11, S)),  # g
    17: ((13, S), (14, S), (19, N), (16, E)),  # h
    18: ((16, S), (19, W), (20, N), (10, S)),  # i
    19: ((17, S), (15, S), (21, N), (18, E)),  # j
    20: ((18, S), (21, W), (22, N), (10, W)),  # k
    21: ((19, S), (15, E), (23, N), (20, E)),  # l
    22: ((20, S), (23, W), (0, N), (4, W)),  # m
    23: ((21, S), (9, E), (1, N), (22, E)),  # n
}

""" Pyramid """
PROBLEM5 = {
    0: ((25, S), (3, N), (2, N), (1, N)),
    1: ((0, W), (2, W), (4, W), (5, N)),
    2: ((0, S), (3, W), (4, N), (1, E)),
    3: ((0, E), (15, N), (4, E), (2, E)),
    4: ((2, S), (3, S), (10, N), (1, S)),
    5: ((1, W), (8, N), (7, N), (6, N)),
    6: ((5, W), (7, W), (9, W), (25, W)),
    7: ((5, S), (8, W), (9, N), (6, E)),
    8: ((5, E), (11, W), (9, E), (7, E)),
    9: ((7, S), (8, S), (21, W), (6, S)),
    10: ((4, S), (13, N), (12, N), (11, N)),
    11: ((10, W), (12, W), (14, W), (8, E)),
    12: ((10, S), (13, W), (14, N), (11, E)),
    13: ((10, E), (16, W), (14, E), (12, E)),
    14: ((12, S), (13, S), (20, N), (11, S)),
    15: ((3, E), (18, N), (17, N), (16, N)),
    16: ((15, W), (17, W), (19, W), (13, E)),
    17: ((15, S), (18, W), (19, N), (16, E)),
    18: ((15, E), (25, E), (19, E), (17, E)),
    19: ((17, S), (18, S), (23, E), (16, S)),
    20: ((14, S), (23, N), (22, N), (21, N)),
    21: ((20, W), (22, W), (24, W), (9, S)),
    22: ((20, S), (23, W), (24, N), (21, E)),
    23: ((20, E), (19, S), (24, E), (22, E)),
    24: ((22, S), (23, S), (25, N), (21, S)),
    25: ((24, S), (18, E), (0, N), (6, W)),
}

""" Crow foot """
PROBLEM6 = {
    0: ((29, S), (3, N), (2, N), (1, N)),
    1: ((0, W), (2, W), (4, W), (5, N)),
    2: ((0, S), (3, W), (4, N), (1, E)),
    3: ((0, E), (15, N), (4, E), (2, E)),
    4: ((2, S), (3, S), (10, N), (1, S)),
    5: ((1, W), (8, N), (7, N), (6, N)),
    6: ((5, W), (7, W), (9, W), (26, W)),
    7: ((5, S), (8, W), (9, N), (6, E)),
    8: ((5, E), (11, W), (9, E), (7, E)),
    9: ((7, S), (8, S), (21, W), (6, S)),
    10: ((4, S), (13, N), (12, N), (11, N)),
    11: ((10, W), (12, W), (14, W), (8, E)),
    12: ((10, S), (13, W), (14, N), (11, E)),
    13: ((10, E), (16, W), (14, E), (12, E)),
    14: ((12, S), (13, S), (20, N), (11, S)),
    15: ((3, E), (18, N), (17, N), (16, N)),
    16: ((15, W), (17, W), (19, W), (13, E)),
    17: ((15, S), (18, W), (19, N), (16, E)),
    18: ((15, E), (28, E), (19, E), (17, E)),
    19: ((17, S), (18, S), (23, E), (16, S)),
    20: ((14, S), (23, N), (22, N), (21, N)),
    21: ((20, W), (22, W), (24, W), (9, S)),
    22: ((20, S), (23, W), (24, N), (21, E)),
    23: ((20, E), (19, S), (24, E), (22, E)),
    24: ((22, S), (23, S), (25, N), (21, S)),
    25: ((24, S), (28, N), (27, N), (26, N)),
    26: ((25, W), (27, W), (29, W), (6, W)),
    27: ((25, S), (28, W), (29, N), (26, E)),
    28: ((25, E), (18, E), (29, E), (27, E)),
    29: ((27, S), (28, S), (0, N), (26, S)),
}


def get_edges(problem):
    sides = {0: 'N', 1: 'E', 2: 'S', 3: 'W'}
    return {'-'.join((min(f'{tile1}{sides[side1]}', f'{tile2}{sides[side2]}'),
                      max(f'{tile1}{sides[side1]}', f'{tile2}{sides[side2]}')))
            for tile1, neighbors in problem.items() for side1, (tile2, side2) in enumerate(neighbors)}


def problem_len(problem):
    num_tiles = len(problem)
    num_edges = 2 * num_tiles
    num_corners = len(list((get_shape_corners(problem))))
    return num_tiles * 9 + num_edges * 3 + num_corners


def verify_problem(problem):
    for k, v in problem.items():
        for i, (p, c) in enumerate(v):
            try:
                assert problem[p][c] == (k, i)
            except AssertionError:
                print(f"Tile {k} does not have {p} to its {i}")


def get_shape_corners(problem: dict[int, tuple[tuple[int, int]]]) -> list[tuple[tuple[int, int]]]:
    tile_corners = [(tile, n) for tile in problem.keys() for n in range(4)]
    corners = [i for i in range(len(tile_corners))]

    def find(i):
        if corners[i] == i: return i
        root = find(corners[i])
        corners[i] = root
        return root

    def union(i, j):
        i = find(i)
        j = find(j)
        if i != j:
            corners[i] = j

    for tile, value in problem.items():
        for k, (t, s) in enumerate(value):
            union(tile * 4 + (k + 1) % 4, t * 4 + s)
            union(tile * 4 + k, t * 4 + (s + 1) % 4)

    tile_corners.sort(key=lambda p: find(4 * p[0] + p[1]))
    return [tuple(g) for _, g in groupby(tile_corners, key=lambda p: find(4 * p[0] + p[1]))]


def get_corner_lookup(shape_corners):
    return {
        tc: [_ for _ in corner if _ != tc]
        for corner in shape_corners for tc in corner
    }


class Orientation(Enum):
    IDENTITY = 1
    R1 = 2
    R2 = 3
    R3 = 4
    F = 5
    R1F = 6
    R2F = 7
    R3F = 8


class Piece:

    def __init__(self, pattern: str, color: Optional[str] = None, index: int = None):
        self._color = color
        self._index = index
        self._orientation = Orientation.IDENTITY
        m = [list(s.strip(' ')) for s in pattern.strip().split('\n')]
        self._full = ((int(''.join(i for i in m[0]), 2) << 11) |
                      (int(''.join(row[-1] for row in m), 2) << 7) |
                      (int(''.join(reversed(m[-1])), 2) << 3) |
                      (int(''.join(row[0] for row in reversed(m)), 2) >> 1))
        self._full_inv = bit_reversal(self._full, 16)

    def set_orientation(self, orientation):
        self._orientation = orientation

    @property
    def full(self):
        match self._orientation:
            case Orientation.IDENTITY:
                return self._full
            case Orientation.R1:
                return circular_lshift(self._full, 12, 16)
            case Orientation.R2:
                return circular_lshift(self._full, 8, 16)
            case Orientation.R3:
                return circular_lshift(self._full, 4, 16)
            case Orientation.F:
                return circular_lshift(self._full_inv, 11, 16)
            case Orientation.R1F:
                return circular_lshift(self._full_inv, 7, 16)
            case Orientation.R2F:
                return circular_lshift(self._full_inv, 3, 16)
            case Orientation.R3F:
                return circular_lshift(self._full_inv, -1, 16)

    @property
    def full_inv(self):
        return bit_reversal(self.full, 16)

    @property
    def north(self):
        return (self.full >> 11) & ((1 << 5) - 1)

    @property
    def east(self):
        return (self.full >> 7) & ((1 << 5) - 1)

    @property
    def south(self):
        return (self.full >> 3) & ((1 << 5) - 1)

    @property
    def west(self):
        return circular_lshift(self.full, 1, 16) & ((1 << 5) - 1)

    @property
    def north_inv(self):
        return self.full_inv & ((1 << 5) - 1)

    @property
    def east_inv(self):
        return (self.full_inv >> 4) & ((1 << 5) - 1)

    @property
    def south_inv(self):
        return (self.full_inv >> 8) & ((1 << 5) - 1)

    @property
    def west_inv(self):
        return circular_lshift(self.full_inv, 4, 16) & ((1 << 5) - 1)

    @property
    def color(self):
        return self._color

    @property
    def index(self):
        return self._index

    def sides(self):
        return self.north, self.east, self.south, self.west

    def get_corner(self, corner):
        mask = (1 << (15 - 4 * corner))
        return 1 if self.full & mask == mask else 0

    def len_corners(self):
        return sum(side & 1 for side in self.sides())

    def get_side_inv(self, side: int):
        match side:
            case 0:
                return self.north_inv
            case 1:
                return self.east_inv
            case 2:
                return self.south_inv
            case 3:
                return self.west_inv

    def __str__(self):
        tl = ' ┌─'
        tr = '─┐ '
        hz = '───'
        bl = ' └─'
        br = '─┘ '
        vt = ' │ '
        sp = '   '
        char_map = {0: sp, 1: tl, 2: tr, 3: hz, 4: bl, 5: vt, 7: br, 8: br, 10: vt, 11: bl, 12: hz, 13: tr, 14: tl,
                    15: sp}

        extended_matrix = [
            ['0'] * 7,
            ['0'] + ['1' if i & self.north else '0' for i in (16, 8, 4, 2, 1)] + ['0'],
            ['0'] + ['1' if self.west & 2 else '0'] + ['1'] * 3 + ['1' if self.east & 8 else '0'] + ['0'],
            ['0'] + ['1' if self.west & 4 else '0'] + ['1'] * 3 + ['1' if self.east & 4 else '0'] + ['0'],
            ['0'] + ['1' if self.west & 8 else '0'] + ['1'] * 3 + ['1' if self.east & 2 else '0'] + ['0'],
            ['0'] + ['1' if i & self.south else '0' for i in (1, 2, 4, 8, 16)] + ['0'],
            ['0'] * 7
        ]
        return '\n'.join(''.join(char_map[int(f'{extended_matrix[i - 1][j - 1]}'
                                              f'{extended_matrix[i - 1][j]}'
                                              f'{extended_matrix[i][j - 1]}'
                                              f'{extended_matrix[i][j]}', 2)]
                                 for j in range(1, 7))[1:].rstrip()
                         for i in range(1, 7))

    def __len__(self):
        edge_len = sum(n & m > 0 for n in self.sides() for m in (8, 4, 2, 1))
        return edge_len + 9


def make_pieces(pad: Pads):
    return [Piece(rows, color=pad.name.lower(), index=i) for i, rows in enumerate(pad.to_list())]


def corners(piece: Piece) -> int:
    return sum((8 << i) & piece.full == (8 << i) for i in range(0, 16, 4))


def mid_cubits(piece: Piece) -> int:
    return sum(((2 << i) & piece.full == (2 << i) for i in range(0, 16, 4)))


def other_cubits(piece: Piece) -> int:
    return sum(((1 << i) & piece.full == (1 << i) for i in range(0, 16, 2)))


def filter_pieces(num_tiles: int, num_corners, pieces: Iterable[Piece]):
    for pcs in combinations(pieces, num_tiles):
        if (
                sum(corners(pc) for pc in pcs) == num_corners and
                sum(mid_cubits(pc) for pc in pcs) == 2 * num_tiles and
                sum(other_cubits(pc) for pc in pcs) == 4 * num_tiles
        ):
            yield pcs


def bit_reversal(n: int, num_bits: int):
    if n == 0: return 0
    d = 1 << (num_bits - 1)
    return reduce(or_, (d // b for i in range(num_bits) if (b := n & (1 << i)) > 0))


def circular_lshift(n, m, num_bits):
    """Returns n <<< m """
    m %= num_bits
    if m == 0: return n
    n <<= m
    mask = ((1 << m) - 1) << num_bits
    return ((mask & n) >> num_bits) | n & ((1 << num_bits) - 1)


def min_tile(rows, num_pieces):
    min_tile, min_count = 0, num_pieces * 8
    for tile, g in groupby(rows, key=lambda row: row[0] // (num_pieces * 8)):
        n = sum(1 for _ in g)
        assert n > 0
        if n < min_count:
            min_tile, min_count = tile, n
    return min_tile, min_count


def solve(tiles: list[int], rows: list[list[int]], solution: list[list[int]], num_pieces, f):
    """
    Generator function that finds all exact covers of arg cubits with rows from arg rows, and yields lists
    where each list contains the rows in arg solution extended with a cover of arg cubits.

    This function may temporarily append rows to arg solution, but will pop them off again such that when
    the function returns, arg solution is unchanged.

    :param tiles: a list of tiles to cover. This list contains only cubits that are not in any word in arg solution
    :param rows: a list of rows from which words are drawn to create each cover. These words contain only cubits that are in arg cubits.
    :param solution: a list of words to prepend to each cover found
    :return: None
    """
    if not tiles:
        # No more tiles to cover; we're done.
        yield solution.copy()
    elif not rows:
        return
    else:
        # heuristic: start with the tile that occurs in the least number of rows
        num_rows_per_tile = num_pieces * 8
        t0, _ = min_tile(rows, num_pieces)
        remaining_tiles = [tile for tile in tiles if tile != t0]
        # Loop invariant: Args tiles, rows, and solution, are not mutated
        rows_for_tile = [row for row in rows if row[0] // num_rows_per_tile == t0]

        for row in rows_for_tile:
            print('Select row:', str_row(row, num_pieces), file=f)
            piece_num, orientation = divmod(row[0] % num_rows_per_tile, 8)
            solution.append(row)
            remaining_rows = [r for r in rows if (
                    r[0] // num_rows_per_tile != t0 and
                    r[0] % num_rows_per_tile // 8 != piece_num and
                    all(row[i] & r[i] == 0 for i in range(1, len(row)))
            )]
            if len(remaining_rows) >= len(remaining_tiles):
                yield from solve(remaining_tiles, remaining_rows, solution, num_pieces, f)
            solution.pop()


def make_row(piece: Piece, orientation: Orientation, tile, problem, shape_corners, row_num: int) -> list[int]:
    corner_lookup = get_corner_lookup(shape_corners)
    piece.set_orientation(orientation)
    src_side = [piece.north_inv, piece.east_inv, piece.south_inv, piece.west_inv]
    target_shifts = [11, 7, 3, -1]
    row = [0] * len(problem)
    row[tile] = piece.full
    for i, (t, s) in enumerate(problem[tile]):
        row[t] = circular_lshift(src_side[i], target_shifts[s], 16)
    for i in range(4):
        if piece.get_corner(i) == 1:
            for t, c in corner_lookup[(tile, i)]:
                row[t] |= 1 << (15 - 4 * c)
    # row.append(pieces.index(piece))
    return [row_num] + row


def solve1(problem, pieces: list[Piece], hints=None):
    shape_corners = get_shape_corners(problem)
    row_numbers = count()
    tiles = list(range(len(problem)))
    rows = [
        make_row(pc, orientation, tile, problem, shape_corners, next(row_numbers))
        for tile in tiles
        for pc in pieces
        for orientation in Orientation
    ]
    with open('log_file.txt', mode='w') as f:
        yield from solve(tiles, rows, [], len(pieces), f)


def str_row(row, num_pieces):
    tile, r = divmod(row[0], num_pieces * 8)
    piece_num, orientation = divmod(r, 8)
    w = [f'{bin(t)[2:].zfill(16)}' for t in row[1:]]
    return f'{tile}-{piece_num}-{orientation}, {w}'


def row_to_tile_map(row, pieces, tiles):
    piece = pieces[row[0] % len(pieces) // 8]
    for tile in tiles:
        for orientation in Orientation:
            piece.set_orientation(orientation)
            if piece.full == row[tile + 1]:
                return (tile, piece)


def possible_pieces_problem6():
    problem = PROBLEM6
    all_pieces = [piece for pad in Pads for piece in make_pieces(pad)]
    # shuffle(all_pieces)
    shape_corners = get_shape_corners(problem)
    with open('possible_piece_selection_problem6.csv', mode='w') as f:
        writer = csv.writer(f)
        for pcs in filter_pieces(len(problem), len(shape_corners), all_pieces):
            print('*', end='')
            writer.writerow(f'{pc.color}[{pc.index}]' for pc in pcs)


def solve_problem6():
    start = time()
    d = {
        f'{p.color}[{p.index}]': p
        for pad in Pads for p in make_pieces(pad)
    }
    with open('possible_piece_selection_problem6.csv', 'r') as f:
        reader = csv.reader(f)
        pieces = [[d[ps] for ps in row] for row in list(reader)]
    try:
        solution = next(solve1(PROBLEM6, pieces[5]))
    except StopIteration:
        pass
    else:
        d = dict(row_to_tile_map(row, pieces, PROBLEM6.keys()) for row in solution)
        for tile in sorted(d.keys()):
            piece = d[tile]
            print(f"{tile}: {piece.color}[{piece.index}]\n{piece}")
    print(f'{(time() - start):.3f}')


def solve_problem(problem, pieces, hints=None):
    start = time()
    try:
        solution = next(solve1(problem, pieces))
    except StopIteration:
        pass
    else:
        d = {}
        rows_per_tile = len(pieces) * 8
        orientations = list(Orientation)
        for row in solution:
            print(str_row(row, len(pieces)))
            tile = row[0] // rows_per_tile
            piece_num, orientation_num = divmod(row[0] % rows_per_tile, 8)
            piece = pieces[piece_num]
            orientation = orientations[orientation_num]
            piece.set_orientation(orientation)
            d[tile] = piece
        for tile in range(len(problem)):
            piece = d[tile]
            print(f'{tile}: {piece.color}[{piece.index}]\n{piece}')
    print(f'{(time() - start):.3f}')


def solve_problem1():
    start = time()
    pieces = make_pieces(Pads.GREEN)
    # shuffle(pieces)
    try:
        solution = next(solve1(PROBLEM1, pieces))
    except StopIteration:
        print('No solution found.')
    else:
        for row in solution:
            print(str_row(row, 6))
    print(f'{(time() - start):.3f}')


if __name__ == '__main__':
    pieces = [p for pad in Pads for p in make_pieces(pad)]
    # pieces = make_pieces(Pads.GREEN) + make_pieces(Pads.BLUE)
    shuffle(pieces)
    solve_problem(PROBLEM4, pieces)
