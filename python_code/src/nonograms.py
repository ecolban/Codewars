from itertools import combinations
from heapq import heapify, heappop, heappush, heapreplace


class Nonogram:

    def __init__(self, all_clues):
        self.column_clues, self.row_clues = all_clues
        self.height = len(self.row_clues)
        self.width = len(self.column_clues)
        # self.board[i][j] == -1 if not yet known whether the value should be 1 or 0
        self.board = [[-1 for _ in range(self.width)] for _ in range(self.height)]
        self.possible_ = {}

    def solve(self):
        queue = [(self.priority(i, 0), i, 0) for i in range(self.height)] \
                + [(self.priority(j, 1), j, 1) for j in range(self.width)]
        heapify(queue)
        count = self.width * self.height
        while count > 0:
            _, i, t = heappop(queue)
            possible = list(self.remove_impossible(i, t) if (i, t) in self.possible_
                            else self.initialize_possible(i, t))
            self.possible_[(i, t)] = possible
            touched = list(self.solve_partial(i, t, possible))
            count -= len(touched)
            for j in touched:
                heappush(queue, (self.priority(j, 1 - t), j, 1 - t))
        return tuple(tuple(self.board[i]) for i in range(self.height))

    @staticmethod
    def free_spaces(clues, length):
        return length - sum(clues) - len(clues) + 1

    @staticmethod
    def get_assignment(clues, combination):
        k = 0
        res = []
        for j in range(len(clues) + len(combination)):
            if j not in combination:
                res += [1] * clues[k]
                k += 1
            res.append(0)
        return tuple(res[:-1])

    def priority(self, i, t):
        if (i, t) in self.possible_:
            return len(self.possible_[(i, t)])
        clues = self.row_clues[i] if t == 0 else self.column_clues[i]
        dof = Nonogram.free_spaces(clues, self.width)
        return choose(len(clues) + dof, dof)

    def initialize_possible(self, i, t):
        clues = self.row_clues[i] if t == 0 else self.column_clues[i]
        dof = Nonogram.free_spaces(clues, self.width if t == 0 else self.height)
        for combination in combinations(range(len(clues) + dof), dof):
            assignment = Nonogram.get_assignment(clues, combination)
            if self.verify_(assignment, i, t):
                yield assignment

    def verify_(self, vs, i, t):
        if t == 0:
            return all(v == self.board[i][c] or self.board[i][c] == -1 for c, v in enumerate(vs))
        else:
            return all(v == self.board[r][i] or self.board[r][i] == -1 for r, v in enumerate(vs))

    def solve_partial(self, i, t, possible):
        for j in range(self.width if t == 0 else self.height):
            r, c = (i, j) if t == 0 else (j, i)
            if self.board[r][c] == -1:
                v = next((v for v in (0, 1) if all(vs[j] == v for vs in possible)), -1)
                if v != -1:
                    self.board[r][c] = v
                    yield j

    def remove_impossible(self, i, t):
        rs = self.possible_[(i, t)]
        return (r for r in rs if self.verify_(r, i, t))

    def __str__(self):
        col_clues_height = max(len(clues) for clues in self.column_clues)
        row_clues_strings = [','.join(str(c) for c in clues) for clues in self.row_clues]
        row_clues_width = max(len(s) for s in row_clues_strings)
        row_separator = '-' * row_clues_width + '|' + '---' * (self.width - 1) + '--|'

        def row_gen():
            # Add column clues
            for i in range(col_clues_height, 0, -1):
                yield (' ' * row_clues_width + '|'
                       + '|'.join(  # join groups of 5 columns
                            ' '.join(  # join 5 consecutive columns
                                '%2d' % self.column_clues[5 * q + r][k] if k >= 0 else '  '
                                for r in range(min(5, self.width - 5 * q))
                                for k in (len(self.column_clues[5 * q + r]) - i,))
                            for q in range((self.width + 4) // 5))
                       + '|')
            yield row_separator
            # Add row clues followed by row for each row of board
            for i, row in enumerate(self.board):
                yield (row_clues_strings[i].rjust(row_clues_width)  # row clues
                       + '|'
                       + '|'.join(  # join groups of 5 columns
                            ' '.join(  # join 5 consecutive columns
                                '%2d' % row[5 * q + r] if row[5 * q + r] in (0, 1) else ' _'
                                for r in range(min(5, self.width - 5 * q)))
                            for q in range((self.width + 4) // 5))  # row values
                       + '|')
                # Add row separator for every 5 rows
                if i % 5 == 4: yield row_separator
            # Add bottom row separator
            if self.height % 5 != 0: yield row_separator

        return '\n'.join(row_gen())


clues_1 = (
    ((2, 3, 1, 1, 4), (2, 1, 3, 1, 3, 3), (1, 2, 6, 2, 1), (1, 2, 3, 1, 1), (6, 1, 2, 1), (6, 9, 1), (2, 3, 2, 7),
     (2, 1, 1, 1, 2, 3), (1, 1, 2, 2, 3, 2), (1, 1, 4, 1, 2, 1), (1, 1, 3, 4, 1, 3, 1), (2, 8, 2, 2),
     (1, 1, 4, 5, 1), (3, 8, 5, 2), (2, 8, 2, 4), (6, 8, 1, 1, 2, 1), (4, 9, 1, 1, 4), (2, 1, 10, 3),
     (1, 2, 3, 1, 2), (3, 4, 1, 1, 2), (4, 2, 8), (2, 1, 8, 5), (13, 3, 2), (5, 7, 1, 2, 2), (4, 9, 3)),
    ((7, 4, 9), (2, 3, 1, 5, 6), (2, 4, 2, 3), (2, 4, 2, 3, 5), (7, 1, 1, 3), (4, 2, 2), (2, 2, 2, 1, 1, 4),
     (4, 15), (4, 1, 3, 5, 6), (2, 9, 4), (2, 1, 1, 9, 4), (2, 1, 2, 8, 4), (1, 1, 11, 4), (1, 3, 1, 4, 1),
     (5, 1, 1, 3, 2), (3, 1, 3, 1, 1), (1, 1, 1, 3, 3), (1, 1, 1, 3, 3), (3, 3, 2, 6, 3), (2, 7, 1, 4),
     (3, 1, 3, 4), (1, 1, 1, 3, 2), (2, 2, 5, 1, 1), (2, 6, 2, 5, 3), (4, 3, 6, 3)))

clues_2 = (((3,), (4,), (2, 2, 2), (2, 4, 2), (6,), (3,)),
           ((4,), (6,), (2, 2), (2, 2), (2,), (2,), (2,), (2,), (), (2,), (2,)))

clues_3 = (((3,), (4,), (2, 2, 1), (2, 4, 2), (6,)),
           ((4,), (5,), (2, 1), (2, 1), (2,), (2,), (2,), (2,), (), (2,), (2,)))

clues_4 = (((3,), (4,), (2, 2, 1), (2, 4, 1), (6,), (3,)),
           ((4,), (6,), (2, 2), (2, 2), (2,), (2,), (2,), (2,), (), (2,)))

clues_5 = (((1, 2, 6), (2, 6), (4, 2, 2), (1, 5, 1), (2, 1, 7, 5), (1, 1, 7, 7), (2, 1, 2, 10), (2, 7), (2, 1, 4, 2),
            (1, 3, 4, 5), (5, 4, 6), (7, 5, 6), (8, 4, 3, 2), (8, 3, 2, 1), (5, 2, 2, 1, 3), (7, 1, 3, 3), (8, 9, 3),
            (5, 3, 10, 1, 1), (9, 1, 1, 4, 5), (1, 9, 2, 3), (3, 4, 5), (1, 1, 2, 2, 1, 1), (4, 1), (1, 4, 2), (2, 4)),
           ((1, 4), (6, 2, 1), (3, 5), (2, 10), (1, 9, 1), (3, 12, 1), (3, 8, 3), (4, 2, 3, 7), (3, 9), (3, 3, 6),
            (2, 1, 2), (3, 4), (1, 1, 3, 2), (1, 1, 4), (3, 7, 2, 1), (3, 13, 1), (13,), (9, 5), (3, 5, 2),
            (9, 3, 2, 5), (3, 9, 1, 9), (2, 3, 5, 3, 3), (2, 3, 3, 10), (3, 3, 4, 3, 1, 1), (3, 10, 3)))


def choose(n, k):
    k = min(k, n - k)
    res = 1
    for i in range(k):
        res = res * (n - i) // (i + 1)
    return res


def test_nonogram():
    ng = Nonogram(clues_5)
    print('dimension = %dx%d' % (ng.height, ng.width))
    from time import time
    start = time()
    ng.solve()
    stop = time()
    print('===================================\n')
    print(ng)
    print('Time = %.2f s' % (stop - start))


def solve(clues, width, height):
    return Nonogram.solve(clues)


if __name__ == "__main__":
    test_nonogram()
