from itertools import permutations


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
SIZE = 6


def pieces_fit(piece1, side1, piece2, side2):
    edge1 = get_edge(piece1, side1)
    edge2 = get_edge(piece2, side2)
    return edges_fit(edge1, edge2, reverse=~(side1 ^ side2) & 1)


def get_edge(piece, side):
    return (
        piece[0] if side == N
        else [piece[k][-1] for k in range(SIZE)] if side == E
        else piece[-1] if side == S
        else [piece[k][0] for k in range(SIZE)]  # if side == W
    )


def edges_fit(edge1, edge2, reverse):
    return (all(edge1[i] + edge2[SIZE - 1 - i if reverse else i] <= 1 for i in (0, SIZE - 1))
            and all(edge1[i] + edge2[SIZE - 1 - i if reverse else i] == 1 for i in range(1, SIZE - 1)))


def solve_snafooz(pieces):
    global SIZE
    SIZE = len(pieces[0])
    p2 = pieces[0]
    d = [[get_piece(pieces[i], orientation) for orientation in ORIENTATIONS] for i in range(1, 6)]
    for n0, n1, n3, n4, n5 in permutations(range(5)):
        for p0 in d[n0]:
            if pieces_fit(p0, S, p2, N):
                for p1 in d[n1]:
                    if pieces_fit(p1, N, p0, W) \
                            and pieces_fit(p1, E, p2, W):
                        for p3 in d[n3]:
                            if pieces_fit(p3, W, p2, E) \
                                    and pieces_fit(p3, N, p0, E):
                                for p4 in d[n4]:
                                    if pieces_fit(p4, N, p2, S) \
                                            and pieces_fit(p4, W, p1, S) \
                                            and pieces_fit(p4, E, p3, S):
                                        for p5 in d[n5]:
                                            if pieces_fit(p5, N, p4, S) \
                                                    and pieces_fit(p5, E, p3, E) \
                                                    and pieces_fit(p5, S, p0, N) \
                                                    and pieces_fit(p5, W, p1, W):
                                                return [p0, p1, p2, p3, p4, p5]


def to_string(solution):
    p0, p1, p2, p3, p4, p5 = solution
    dashes = '-' * SIZE
    spaces = ' ' * (SIZE + 1)
    s = [
        f'{spaces}+{dashes}+',
        '\n'.join(f'{spaces}|{"".join("*" if e == 1 else " " for e in p0[r])}|' for r in range(SIZE)),
        f'+{dashes}+{dashes}+{dashes}+',
        '\n'.join(f'|{"".join("*" if e == 1 else " " for e in p1[r])}'
                  f'|{"".join("*" if e == 1 else " " for e in p2[r])}'
                  f'|{"".join("*" if e == 1 else " " for e in p3[r])}|' for r in range(SIZE)),
        f'+{dashes}+{dashes}+{dashes}+',
        '\n'.join(f'{spaces}|{"".join("*" if e == 1 else " " for e in p4[r])}|' for r in range(SIZE)),
        f'{spaces}+{dashes}+',
        '\n'.join(f'{spaces}|{"".join("*" if e == 1 else " " for e in p5[r])}|' for r in range(SIZE)),
        f'{spaces}+{dashes}+',
    ]
    return '\n'.join(s)


if __name__ == '__main__':
    from time import time

    pieces1 = [
        [[0, 0, 1, 1, 0, 0],
         [0, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 0],
         [0, 1, 1, 1, 1, 0],
         [1, 1, 1, 1, 1, 1],
         [1, 0, 1, 0, 1, 1]],

        [[0, 1, 0, 0, 1, 1],
         [1, 1, 1, 1, 1, 1],
         [0, 1, 1, 1, 1, 0],
         [1, 1, 1, 1, 1, 0],
         [0, 1, 1, 1, 1, 1],
         [0, 0, 1, 1, 0, 1]],

        [[0, 0, 1, 1, 0, 1],
         [1, 1, 1, 1, 1, 1],
         [0, 1, 1, 1, 1, 0],
         [1, 1, 1, 1, 1, 0],
         [0, 1, 1, 1, 1, 1],
         [0, 0, 1, 1, 0, 0]],

        [[0, 0, 1, 1, 0, 0],
         [0, 1, 1, 1, 1, 0],
         [1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1],
         [0, 1, 1, 1, 1, 0],
         [0, 1, 0, 0, 1, 0]],

        [[0, 0, 1, 1, 0, 1],
         [1, 1, 1, 1, 1, 1],
         [0, 1, 1, 1, 1, 0],
         [0, 1, 1, 1, 1, 0],
         [1, 1, 1, 1, 1, 1],
         [1, 1, 0, 0, 1, 1]],

        [[0, 0, 1, 1, 0, 0],
         [0, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 0],
         [1, 1, 1, 1, 1, 0],
         [0, 1, 1, 1, 1, 1],
         [0, 1, 0, 0, 1, 0]],
    ]
    pieces2 = [
        [[0, 0, 1, 0, 0],
         [1, 1, 1, 1, 0],
         [0, 1, 1, 1, 1],
         [1, 1, 1, 1, 0],
         [0, 0, 1, 0, 0]],
        [[1, 0, 1, 0, 0],
         [1, 1, 1, 1, 1],
         [0, 1, 1, 1, 0],
         [1, 1, 1, 1, 1],
         [0, 0, 1, 1, 0]],
        [[1, 1, 0, 1, 1],
         [0, 1, 1, 1, 0],
         [1, 1, 1, 1, 1],
         [0, 1, 1, 1, 0],
         [0, 1, 1, 0, 0]],
        [[0, 1, 0, 1, 0],
         [0, 1, 1, 1, 1],
         [1, 1, 1, 1, 0],
         [0, 1, 1, 1, 1],
         [0, 0, 0, 1, 0]],
        [[1, 1, 0, 0, 0],
         [0, 1, 1, 1, 0],
         [1, 1, 1, 1, 1],
         [0, 1, 1, 1, 0],
         [1, 1, 0, 1, 0]],
        [[1, 0, 0, 1, 1],
         [1, 1, 1, 1, 1],
         [0, 1, 1, 1, 0],
         [1, 1, 1, 1, 1],
         [0, 1, 1, 0, 1]]
    ]
    start = time()
    solution = solve_snafooz(pieces2)
    print(to_string(solution))
    print(f'time = {round((time() - start) * 1000)} ms')
    start = time()
    solution = solve_snafooz(pieces1)
    print(to_string(solution))
    print(f'time = {round((time() - start) * 1000)} ms')
