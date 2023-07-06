from heapq import heappop, heappush, heapify
from random import randrange
from typing import Optional


def identity(r, c):
    return r, c


def flip(r, c):
    return r, SIZE - 1 - c


def rot90(r, c):
    return SIZE - 1 - c, r


def rot90f(r, c):
    return c, r


def rot180(r, c):
    return SIZE - 1 - r, SIZE - 1 - c


def rot180f(r, c):
    return SIZE - 1 - r, c


def rot270(r, c):
    return c, SIZE - 1 - r


def rot270f(r, c):
    return SIZE - 1 - c, SIZE - 1 - r


def get_piece(piece, orientation):
    return [[piece[i][j] for c in range(SIZE) for i, j in (orientation(r, c),)] for r in range(SIZE)]


ORIENTATIONS = identity, flip, rot90, rot90f, rot180, rot180f, rot270, rot270f
N, W, E, S = 0, 1, 2, 3
SIZE = 7

NUM_ORIENTATIONS = len(ORIENTATIONS)

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


class Piece:

    def __init__(self, pattern: str, color: Optional[str] = None):
        self._pattern = pattern
        self._color = color
        self._orientation = ORIENTATIONS[0]
        m = [list(s.strip(' ')) for s in pattern.strip().split('\n')]
        self._north = int(''.join(i for i in m[0]), 2)
        self._north_inv = int(''.join(i for i in reversed(m[0])), 2)
        self._east = int(''.join(row[-1] for row in m), 2)
        self._east_inv = int(''.join(row[-1] for row in reversed(m)), 2)
        self._south = int(''.join(m[-1]), 2)
        self._south_inv = int(''.join(reversed(m[-1])), 2)
        self._west = int(''.join(row[0] for row in m), 2)
        self._west_inv = int(''.join(row[0] for row in reversed(m)), 2)

    def set_orientation(self, orientation):
        self._orientation = orientation

    @property
    def north(self):
        m = {
            identity.__name__: self._north,
            flip.__name__: self._north_inv,
            rot90.__name__: self._west_inv,
            rot180.__name__: self._south_inv,
            rot270.__name__: self._east,
            rot90f.__name__: self._west,
            rot180f.__name__: self._south,
            rot270f.__name__: self._east_inv,
        }
        return m[self._orientation.__name__]

    @property
    def east(self):
        m = {
            identity.__name__: self._east,
            flip.__name__: self._west,
            rot90.__name__: self._north,
            rot180.__name__: self._west_inv,
            rot270.__name__: self._south_inv,
            rot90f.__name__: self._south,
            rot180f.__name__: self._east_inv,
            rot270f.__name__: self._north_inv,
        }
        return m[self._orientation.__name__]

    @property
    def south(self):
        m = {
            identity.__name__: self._south,
            flip.__name__: self._south_inv,
            rot90.__name__: self._east_inv,
            rot180.__name__: self._north_inv,
            rot270.__name__: self._west,
            rot90f.__name__: self._east,
            rot180f.__name__: self._north,
            rot270f.__name__: self._west_inv,
        }
        return m[self._orientation.__name__]

    @property
    def west(self):
        m = {
            identity.__name__: self._west,
            flip.__name__: self._east,
            rot90.__name__: self._south,
            rot180.__name__: self._east_inv,
            rot270.__name__: self._north_inv,
            rot90f.__name__: self._north,
            rot180f.__name__: self._west_inv,
            rot270f.__name__: self._south_inv,
        }
        return m[self._orientation.__name__]

    @property
    def north_inv(self):
        m = {
            identity.__name__: self._north_inv,
            flip.__name__: self._north,
            rot90.__name__: self._west,
            rot180.__name__: self._south,
            rot270.__name__: self._east_inv,
            rot90f.__name__: self._west_inv,
            rot180f.__name__: self._south_inv,
            rot270f.__name__: self._east,
        }
        return m[self._orientation.__name__]

    @property
    def east_inv(self):
        m = {
            identity.__name__: self._east_inv,
            flip.__name__: self._west_inv,
            rot90.__name__: self._north_inv,
            rot180.__name__: self._west,
            rot270.__name__: self._south,
            rot90f.__name__: self._south_inv,
            rot180f.__name__: self._east,
            rot270f.__name__: self._north,
        }
        return m[self._orientation.__name__]

    @property
    def south_inv(self):
        m = {
            identity.__name__: self._south_inv,
            flip.__name__: self._south,
            rot90.__name__: self._east,
            rot180.__name__: self._north,
            rot270.__name__: self._west_inv,
            rot90f.__name__: self._east_inv,
            rot180f.__name__: self._north_inv,
            rot270f.__name__: self._west,
        }
        return m[self._orientation.__name__]

    @property
    def west_inv(self):
        m = {
            identity.__name__: self._west_inv,
            flip.__name__: self._east_inv,
            rot90.__name__: self._south_inv,
            rot180.__name__: self._east,
            rot270.__name__: self._north,
            rot90f.__name__: self._north_inv,
            rot180f.__name__: self._west,
            rot270f.__name__: self._south,
        }
        return m[self._orientation.__name__]

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
        extended_matrix = get_piece(
            [['0'] * SIZE] + [(['0'] + list(row.strip()) + ['0']) for row in self._pattern.split()] + [['0'] * SIZE],
            self._orientation,
        )
        return '\n'.join(''.join(char_map[int(f'{extended_matrix[i - 1][j - 1]}'
                                              f'{extended_matrix[i - 1][j]}'
                                              f'{extended_matrix[i][j - 1]}'
                                              f'{extended_matrix[i][j]}', 2)]
                                 for j in range(1, SIZE))[1:].rstrip()
                         for i in range(1, SIZE))

    @property
    def color(self):
        return self._color


def pieces_fit(piece1, side1, piece2, side2):
    edge1 = get_edge(piece1, side1)
    edge2 = get_edge(piece2, side2, inv=~(side1 ^ side2) & 1)
    return edge1 & edge2 == 0 and (edge1 ^ edge2) & 14 == 14


def get_edge(piece: Piece, side, inv=False):
    return (
        piece.north if side == N
        else piece.east if side == E
        else piece.south if side == S
        else piece.west  # if side == W
    ) if not inv else (
        piece.north_inv if side == N
        else piece.east_inv if side == E
        else piece.south_inv if side == S
        else piece.west_inv  # if side == W
    )


def edges_fit(edge1, edge2, reverse):
    return (all(edge1[i] + edge2[SIZE - 1 - i if reverse else i] <= 1 for i in (0, SIZE - 1))  # corners
            and all(edge1[i] + edge2[SIZE - 1 - i if reverse else i] == 1 for i in range(1, SIZE - 1)))  # rest


# N, W, E, S = 0, 1, 2, 3
#  A
# BCD
#  E
#  F
PROBLEM1 = {
    'A': (('F', S), ('B', N), ('D', N), ('C', N)),
    'B': (('A', W), ('F', W), ('C', W), ('E', W)),
    'C': (('A', S), ('B', E), ('D', W), ('E', N)),
    'D': (('A', E), ('C', E), ('F', E), ('E', E)),
    'E': (('C', S), ('B', S), ('D', S), ('F', N)),
    'F': (('E', S), ('B', W), ('D', E), ('A', N)),
}

# N, W, E, S = 0, 1, 2, 3
#  AB
# CDEF
#  GH
#  IJ
PROBLEM2 = {
    'A': (('I', S), ('C', N), ('B', W), ('D', N)),
    'B': (('J', S), ('A', E), ('F', N), ('E', N)),
    'C': (('A', W), ('I', W), ('D', W), ('G', W)),
    'D': (('A', S), ('C', E), ('E', W), ('G', N)),
    'E': (('B', S), ('D', E), ('F', W), ('H', N)),
    'F': (('B', E), ('E', E), ('J', E), ('H', E)),
    'G': (('D', S), ('C', S), ('H', W), ('I', N)),
    'H': (('E', S), ('G', E), ('F', S), ('J', N)),
    'I': (('G', S), ('C', W), ('J', W), ('A', N)),
    'J': (('H', S), ('I', E), ('F', E), ('B', N)),

}
PROBLEM2_CORNERS = [
    (('A', N, E), ('J', S, W)),
    (('A', S, E), ('E', N, W)),
    (('B', N, W), ('I', S, E)),
    (('B', S, W), ('D', N, E)),
    (('D', N, E), ('B', S, W)),
    (('D', S, E), ('H', N, W)),
    (('E', N, W), ('A', S, E)),
    (('E', S, W), ('G', N, E)),
    (('G', N, E), ('E', S, W)),
    (('G', S, E), ('J', N, W)),
    (('H', N, W), ('D', S, E)),
    (('H', S, W), ('I', N, E)),
    (('I', N, E), ('H', S, W)),
    (('I', S, E), ('B', N, W)),
    (('J', N, W), ('G', S, E)),
    (('J', S, W), ('A', N, E)),
]
# N, W, E, S = 0, 1, 2, 3
#  ABC
# DEFGH
#  IJK
#  LMN
PROBLEM3 = {
    'A': (('L', S), ('D', N), ('B', W), ('E', N)),
    'B': (('M', S), ('A', E), ('C', W), ('F', N)),
    'C': (('N', S), ('B', E), ('H', N), ('G', N)),
    'D': (('A', W), ('L', W), ('E', W), ('I', W)),
    'E': (('A', S), ('D', E), ('F', W), ('I', N)),
    'F': (('B', S), ('E', E), ('G', W), ('J', N)),
    'G': (('C', S), ('F', E), ('H', W), ('K', N)),
    'H': (('C', E), ('G', E), ('N', E), ('K', E)),
    'I': (('E', S), ('D', S), ('J', W), ('L', N)),
    'J': (('F', S), ('I', E), ('K', W), ('M', N)),
    'K': (('G', S), ('J', E), ('H', S), ('N', N)),
    'L': (('I', S), ('D', W), ('M', W), ('A', N)),
    'M': (('J', S), ('L', E), ('N', W), ('B', N)),
    'N': (('K', S), ('M', E), ('H', E), ('C', N)),
}
PROBLEM3_CORNERS = [
    (('A', N, E), ('M', S, W)),
    (('A', S, E), ('F', N, W)),
    (('B', N, W), ('N', S, E)),
    (('B', S, W), ('D', N, E)),
    (('D', N, E), ('B', S, W)),
    (('D', S, E), ('H', N, W)),
    (('E', N, W), ('A', S, E)),
    (('E', S, W), ('G', N, E)),
    (('G', N, E), ('E', S, W)),
    (('G', S, E), ('J', N, W)),
    (('H', N, W), ('D', S, E)),
    (('H', S, W), ('I', N, E)),
    (('I', N, E), ('H', S, W)),
    (('I', S, E), ('B', N, W)),
    (('J', N, W), ('G', S, E)),
    (('J', S, W), ('A', N, E)),
]


def to_list(color, color_str):
    return [Piece(rows, color_str) for rows in color.split('\n\n')]


def get_corner(piece, side1, side2):
    return (
        ((piece.north if side2 == E else piece.north_inv) & 1) if side1 == N else
        ((piece.south if side2 == E else piece.south_inv) & 1)
    )


def verify_problem(problem):
    for k, v in problem.items():
        for i, (p, c) in enumerate(v):
            try:
                assert problem[p][c] == (k, i)
            except AssertionError:
                print(f"Tile {k} does not have {p} to its {i}")


def solve(problem, problem_corners, pieces):
    solution = {k: None for k in problem}
    solution['D'] = (0, 0)
    remaining_pieces: list[int] = list(range(1, len(pieces)))

    def get_piece_from_index(i: int, j: int):
        pieces[i].set_orientation(ORIENTATIONS[j])
        return pieces[i]

    def fit_solution(tile, piece, orientation):
        piece1 = get_piece_from_index(piece, orientation)
        return (
                all(pieces_fit(piece1, side1, get_piece_from_index(*solution[tile2]), side2)
                    for side1, (tile2, side2) in zip(range(4), problem[tile])
                    if solution[tile2] is not None) and
                all(get_corner(piece1, s1, s2) + get_corner(get_piece_from_index(*solution[tile2]), s3, s4) <= 1
                    for (tile1, s1, s2), (tile2, s3, s4) in problem_corners
                    if tile1 == tile and solution[tile2] is not None)
        )

    def solution_gen():
        nonlocal remaining_pieces
        if not any(v is None for v in solution.values()):
            yield {k: (v[0], get_piece_from_index(*v)) for k, v in solution.items()}
            return
        # if not remaining_pieces: return
        tile = min(
            (tile for tile, v in solution.items() if v is None),
            key=lambda tile: sum(fit_solution(tile, i, j) for i in remaining_pieces for j in range(NUM_ORIENTATIONS)),
        )
        possible: list[tuple[int, int]] = [
            (i, j) for i in remaining_pieces for j in range(NUM_ORIENTATIONS) if fit_solution(tile, i, j)
        ]
        for piece_index, orientation_index in possible:
            solution[tile] = (piece_index, orientation_index)
            remaining_pieces_ = remaining_pieces
            remaining_pieces = [i for i in remaining_pieces if i != piece_index]
            yield from solution_gen()
            remaining_pieces = remaining_pieces_
        solution[tile] = None

    return solution_gen()


def random_matrix(m: int, n: int, happy_cube: bool = False) -> list[list[int]]:
    res = [[0] * n for _ in range(m)]
    r = [[randrange(1, 100) for _ in range(n)] for _ in range(m)]
    if happy_cube:
        for i in range(1, n - 1):
            for j in range(1, m - 1):
                res[i][j] = 1
        q = ([(r[0][j], 0, j) for j in range(1, n - 1)] +
             [(r[m - 1][j], m - 1, j) for j in range(1, n - 1)] +
             [(r[i][0], i, 0) for i in range(1, m - 1)] +
             [(r[i][n - 1], i, n - 1) for i in range(1, m - 1)])
        heapify(q)
    else:
        q = [(r[m // 2][n // 2], m // 2, n // 2)]
    first_row, last_row, first_col, last_col = 0, 0, 0, 0
    while not all((first_row > 0, last_row > 0, first_col > 0, last_col > 0)):
        _, i, j = heappop(q)
        if res[i][j]: continue
        res[i][j] = 1
        if i == 0:
            first_row += 1
        if i == m - 1:
            last_row += 1
        if j == 0:
            first_col += 1
        if j == n - 1:
            last_col += 1

        for x, y in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
            if 0 <= x < m and 0 <= y < n and not res[x][y]:
                heappush(q, (r[x][y], x, y))

    def remove_cross_hairs():
        change = False
        for i in range(1, m):
            for j in range(1, n):
                if (res[i - 1][j - 1], res[i - 1][j], res[i][j - 1], res[i][j]) in ((1, 0, 0, 1), (0, 1, 1, 0)):
                    res[i - 1][j - 1] = 1
                    res[i - 1][j] = 1
                    change = True
        return change

    while remove_cross_hairs():
        pass
    return res


def outline(matrix: list[list[int]]) -> str:
    m, n = len(matrix) + 2, len(matrix[0]) + 2
    M = [[0] * n] + [[0] + row + [0] for row in matrix] + [[0] * n]
    a = ['   ', ' ┌─', '─┐ ', '───', ' └─', ' │ ', '─┼─', '─┘ ', '─┘ ', '─┼─', ' │ ', ' └─', '───', '─┐ ', ' ┌─', '   ']
    return '\n'.join(''.join(a[int(f'{M[i - 1][j - 1]}{M[i - 1][j]}{M[i][j - 1]}{M[i][j]}', 2)]
                             for j in range(1, n))[1:].rstrip() for i in range(1, m))


if __name__ == '__main__':
    a = random_matrix(20, 20, happy_cube=False)
    print(outline(a))  # from time import time
    #
    # pieces = to_list(GREEN, 'green') + to_list(PINK, 'pink')
    # start = time()
    # solutions = solve(PROBLEM2, PROBLEM2_CORNERS, pieces)
    # try:
    #     solution = next(solutions)
    #     for k, (n, v) in solution.items():
    #         print(f"{k}({pieces[n].color})\n{v}")
    # except StopIteration:
    #     print("No solution found")
    # print(f'time = {round((time() - start) * 1000)} ms')
