from enum import Enum
from itertools import groupby, combinations
from random import shuffle
from time import time
from typing import Optional

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

    OLD_BLUE = """
    11011
    11110
    01111
    11110
    01010
    
    00101
    11111
    01110
    11111
    01010
    
    01011
    01111
    11110
    01111
    01010
    
    00100
    01110
    11111
    01110
    00100
    
    10101
    11111
    01110
    11111
    10101
    
    00100
    01111
    11110
    01111
    00100
    """

    OLD_ORANGE = """
    01010
    11110
    01111
    01110
    00100
    
    01100
    11110
    01111
    11110
    01011
    
    10101
    11111
    01110
    11111
    00100
    
    11011
    01110
    11110
    01111
    11010
    
    00100
    11111
    11111
    01110
    00100
    
    01010
    01111
    01110
    11111
    10101
    """

    OLD_YELLOW = """
    11010
    01110
    11111
    01110
    01010
    
    01011
    11110
    01111
    11110
    00100
    
    00101
    11111
    01110
    11111
    10101
    
    00101
    11111
    01111
    11110
    10100
    
    01010
    01111
    01110
    11111
    10100
    
    01010
    01111
    11110
    01111
    00100
    """

    OLD_PURPLE = """
    00010
    01111
    11110
    01111
    00100
    
    11000
    01111
    11111
    01110
    01010
    
    01011
    01111
    01111
    11110
    00100
    
    11010
    01110
    11110
    01111
    01011
    
    10100
    11110
    11111
    01111
    01101
    
    11011
    11110
    01111
    01110
    01010
    """

    OLD_RED = """
    00100
    11110
    01111
    11110
    00100
    
    10100
    11111
    01110
    11111
    00110
    
    11011
    01110
    11111
    01110
    01100
    
    01010
    01111
    11110
    01111
    00010
    
    11000
    01110
    11111
    01110
    11010
    
    10011
    11111
    01110
    11111
    01101
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
        self._north = int(''.join(i for i in m[0]), 2)
        self._north_inv = int(''.join(i for i in reversed(m[0])), 2)
        self._east = int(''.join(row[-1] for row in m), 2)
        self._east_inv = int(''.join(row[-1] for row in reversed(m)), 2)
        self._south = int(''.join(reversed(m[-1])), 2)
        self._south_inv = int(''.join(m[-1]), 2)
        self._west = int(''.join(row[0] for row in reversed(m)), 2)
        self._west_inv = int(''.join(row[0] for row in m), 2)

    def set_orientation(self, orientation):
        self._orientation = orientation

    @property
    def north(self):
        return {
            Orientation.IDENTITY: self._north,
            Orientation.R1: self._west,
            Orientation.R2: self._south,
            Orientation.R3: self._east,
            Orientation.F: self._north_inv,
            Orientation.R1F: self._east_inv,
            Orientation.R2F: self._south_inv,
            Orientation.R3F: self._west_inv,
        }[self._orientation]

    @property
    def east(self):
        return {
            Orientation.IDENTITY: self._east,
            Orientation.R1: self._north,
            Orientation.R2: self._west,
            Orientation.R3: self._south,
            Orientation.F: self._west_inv,
            Orientation.R1F: self._north_inv,
            Orientation.R2F: self._east_inv,
            Orientation.R3F: self._south_inv,
        }[self._orientation]

    @property
    def south(self):
        return {
            Orientation.IDENTITY: self._south,
            Orientation.R1: self._east,
            Orientation.R2: self._north,
            Orientation.R3: self._west,
            Orientation.F: self._south_inv,
            Orientation.R1F: self._west_inv,
            Orientation.R2F: self._north_inv,
            Orientation.R3F: self._east_inv,
        }[self._orientation]

    @property
    def west(self):
        return {
            Orientation.IDENTITY: self._west,
            Orientation.R1: self._south,
            Orientation.R2: self._east,
            Orientation.R3: self._north,
            Orientation.F: self._east_inv,
            Orientation.R1F: self._south_inv,
            Orientation.R2F: self._west_inv,
            Orientation.R3F: self._north_inv,
        }[self._orientation]

    @property
    def north_inv(self):
        return {
            Orientation.IDENTITY: self._north_inv,
            Orientation.R1: self._west_inv,
            Orientation.R2: self._south_inv,
            Orientation.R3: self._east_inv,
            Orientation.F: self._north,
            Orientation.R1F: self._east,
            Orientation.R2F: self._south,
            Orientation.R3F: self._west,
        }[self._orientation]

    @property
    def east_inv(self):
        return {
            Orientation.IDENTITY: self._east_inv,
            Orientation.R1: self._north_inv,
            Orientation.R2: self._west_inv,
            Orientation.R3: self._south_inv,
            Orientation.F: self._west,
            Orientation.R1F: self._north,
            Orientation.R2F: self._east,
            Orientation.R3F: self._south,
        }[self._orientation]

    @property
    def south_inv(self):
        return {
            Orientation.IDENTITY: self._south_inv,
            Orientation.R1: self._east_inv,
            Orientation.R2: self._north_inv,
            Orientation.R3: self._west_inv,
            Orientation.F: self._south,
            Orientation.R1F: self._west,
            Orientation.R2F: self._north,
            Orientation.R3F: self._east,
        }[self._orientation]

    @property
    def west_inv(self):
        return {
            Orientation.IDENTITY: self._west_inv,
            Orientation.R1: self._south_inv,
            Orientation.R2: self._east_inv,
            Orientation.R3: self._north_inv,
            Orientation.F: self._east,
            Orientation.R1F: self._south,
            Orientation.R2F: self._west,
            Orientation.R3F: self._north
        }[self._orientation]

    @property
    def color(self):
        return self._color

    @property
    def index(self):
        return self._index

    def sides(self):
        return self.north, self.east, self.south, self.west

    def get_corner(self, corner):
        match corner:
            case 0:
                return self.west & 1
            case 1:
                return self.north & 1
            case 2:
                return self.east & 1
            case 3:
                return self.south & 1

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

    @staticmethod
    def make_pieces(color: Pads):
        return [Piece(rows, color.name.lower(), index=i) for i, rows in enumerate(color.to_list())]


def solve(problem, pieces: list[Piece]):
    shape_corners = get_shape_corners(problem)
    corner_lookup = get_corner_lookup(shape_corners)
    solution = {k: None for k in problem}
    remaining_pieces: list[Piece] = pieces

    def filter_pieces():
        num_tiles = len(problem)
        len_tiles = num_tiles * 15 + len(shape_corners)
        for pcs in combinations(pieces, num_tiles):
            if sum(len(pc) for pc in pcs) == len_tiles and sum(pc.len_corners() for pc in pcs) == len(shape_corners):
                yield pcs



    def fit_solution(tile: int, piece: Piece, orientation: Orientation):
        piece.set_orientation(orientation)
        sides = (piece.north, piece.east, piece.south, piece.west)

        def check_corner(corner):
            neighbors = corner_lookup[(tile, corner)]
            solved_neighbors = [(t, c) for t, c in neighbors if solution[t] is not None]
            last = len(solved_neighbors) == len(neighbors)
            corner_cover = sum(solution[t].get_corner(c) for t, c in solved_neighbors) + piece.get_corner(corner)
            return corner_cover == 1 if last else corner_cover <= 1

        return (
                all(pieces_fit(side, p.get_side_inv(s)) for side, (t, s) in zip(sides, problem[tile])
                    if (p := solution[t]) is not None) and
                all(check_corner(corner) for corner in range(4))
        )

    def solution_gen():
        nonlocal remaining_pieces
        if not any(v is None for v in solution.values()):
            yield {tile: piece for tile, piece in solution.items()}, remaining_pieces
            return
        # if not remaining_pieces: return
        tile = min(
            (tile for tile, v in solution.items() if v is None),
            key=lambda tile: sum(fit_solution(tile, piece, orientation)
                                 for piece in remaining_pieces for orientation in Orientation),
        )
        possible: list[tuple[Piece, Orientation]] = [
            (piece, orientation) for piece in remaining_pieces for orientation in Orientation
            if fit_solution(tile, piece, orientation)
        ]
        for piece, orientation in possible:
            piece.set_orientation(orientation)
            solution[tile] = piece
            remaining_pieces_ = remaining_pieces
            remaining_pieces = [pc for pc in remaining_pieces if pc != piece]
            yield from solution_gen()
            remaining_pieces = remaining_pieces_
        solution[tile] = None

    for pieces_ in filter_pieces():
        remaining_pieces = pieces_
        yield from solution_gen()


def pieces_fit(edge1, edge2):
    return edge1 & edge2 == 0 and (edge1 ^ edge2) & 14 == 14


def main_1():
    pads = [
        # Pads.YELLOW,
        Pads.GREEN,
        # Pads.PINK,
        # Pads.RED,
        # Pads.PURPLE,
        Pads.BLUE,
    ]
    problem = PROBLEM2
    pieces = [piece for pad in pads for piece in Piece.make_pieces(pad)]
    shuffle(pieces)
    start = time()
    solutions = solve(problem, pieces)
    try:
        solution, remaining_pieces = next(solutions)
        for tile, piece in solution.items():
            print(f"{tile}({piece.color}[{piece.index}])\n{piece}")
    except StopIteration:
        print('No solution found')

    print(f'time = {round((time() - start) * 1000)} ms')


if __name__ == '__main__':
    main_1()
