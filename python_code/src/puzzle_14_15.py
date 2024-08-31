import heapq
import os
import time
from dataclasses import dataclass


def slide_puzzle(ar: list[list[int]]) -> list[int] | None:
    start_state = tuple(tuple(row) for row in ar)
    print_state(start_state)
    if (parity(start_state) + manhattan_distance(start_state)) % 2 != 0:
        return None
    return a_star(start_state)


# Directions for moving tiles: (row change, column change)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right


@dataclass
class Cons:
    head: int
    tail: 'Cons' = None

    def __iter__(self):
        t: Cons = self
        while t is not None:
            yield t.head
            t = t.tail

    def __lt__(self, other: 'Cons'):
        if other is None:
            return False
        if self.head != other.head:
            return self.head < other.head
        return self.tail < other.tail


# Heuristic function: Manhattan distance
def manhattan_distance(state):
    return sum(
        abs(i - goal_i) + abs(j - goal_j)
        for i, row in enumerate(state)
        for j, value in enumerate(row) if value > 0
        for goal_i, goal_j in (divmod(value - 1, len(row)),)
    )


def parity(state):
    n = len(state) ** 2
    permutation = [(v - 1) % n for row in state for v in row]
    visited = [False] * n
    res = 0
    for i, t in enumerate(visited):
        if not t:
            x, count = i, 0
            while not visited[x]:
                visited[x] = True
                count += 1
                x = permutation[x]
            if count > 1:
                res += count - 1

    return res % 2


# Find the position of the empty tile (0)
def find_empty_tile(state):
    return next((i, j) for i, row in enumerate(state) for j, v in enumerate(row) if v == 0)


# Apply a move and return the new state
def move_tile(state, empty_pos, direction):
    dim = len(state)
    x, y = empty_pos
    dx, dy = direction
    x_, y_ = x + dx, y + dy
    # Check if the move is within bounds
    if 0 <= x_ < dim and 0 <= y_ < dim:
        new_state = tuple((row if i not in (x, x_) else
                           tuple(0 if (i, j) == (x_, y_) else state[x_][y_] if (i, j) == (x, y) else v
                                 for j, v in enumerate(row)))
                          for i, row in enumerate(state))
        return new_state, (x_, y_)
    return None, empty_pos


def is_goal(state):
    n = len(state)
    return all(v == (i * n + j + 1) % n ** 2 for i, row in enumerate(state) for j, v in enumerate(row))


# A* search algorithm
def a_star(start_state) -> list[int] | None:
    num_rows = len(start_state)

    empty_pos = find_empty_tile(start_state)
    pq = []  # Priority queue (min-heap)
    visited = set()  # Dict mapping visited states to their lowest g score found so far
    initial_cost = manhattan_distance(start_state)
    heapq.heappush(pq, (
        initial_cost, 0, initial_cost, start_state, empty_pos, None))  # (priority, g, state, empty_pos, path)

    while pq:
        _, g, h, state, empty_pos, path = heapq.heappop(pq)

        if is_goal(state):
            return list(path)[::-1]

        # Avoid revisiting states
        if state in visited:
            continue
        visited.add(state)

        # Try all possible moves
        for direction in DIRECTIONS:
            state_, empty_pos_ = move_tile(state, empty_pos, direction)
            i, j = empty_pos_  # n moved from where the empty spot is now...
            i_, j_ = empty_pos  # to where the empty spot was before
            n = state[i][j]

            if state_:
                goal_i, goal_j = divmod(n - 1, num_rows)
                h_ = h + ((abs(i_ - goal_i) - abs(i - goal_i)) if i_ != i else (abs(j_ - goal_j) - abs(j - goal_j)))
                g_ = g + 1
                f_ = g_ + h_
                heapq.heappush(pq, (f_, g_, h_, state_, empty_pos_, Cons(n, path)))

    return None  # No solution found

def update_h(row_len, n, i, j, i_, j_):
    goal_i, goal_j = divmod(n - 1, row_len)
    manhattan_increase =

# Function to visualize the solution
def print_state(state):
    for row in state:
        print(' '.join(f'{tile:2d}' if tile != 0 else '  ' for tile in row))


def visualize_solution(solution_path):
    # Loop through each move in the solution
    for step, state in enumerate(solution_path):
        os.system('clear')  # Clear the screen (use 'cls' for Windows)
        print(f"Step {step + 1}:")
        print_state(state)
        time.sleep(0.5)  # Pause for half a second to visualize each step


if __name__ == '__main__':
    # Example of a solvable puzzle state
    example_start_state = [
        [12, 9, 11, 3],
        [5, 14, 7, 4],
        [6, 10, 2, 8],
        [1, 13, 0, 15],
    ]
    simple_example = [
        [1, 2, 3, 4],
        [5, 0, 6, 8],
        [9, 10, 7, 11],
        [13, 14, 15, 12],
    ]
    big_puzzle = [
        [12, 11, 1, 54, 2, 4, 7, 19, 10, 25],
        [32, 53, 5, 27, 46, 22, 28, 38, 20, 30],
        [33, 44, 14, 68, 6, 18, 76, 37, 9, 8],
        [23, 42, 3, 26, 64, 17, 15, 69, 0, 36],
        [21, 63, 13, 43, 86, 95, 79, 73, 29, 70],
        [41, 52, 51, 94, 57, 66, 24, 85, 78, 47],
        [61, 72, 83, 75, 35, 60, 48, 56, 80, 39],
        [81, 65, 31, 55, 49, 50, 87, 16, 40, 89],
        [91, 82, 58, 67, 96, 45, 74, 77, 59, 88],
        [92, 62, 71, 93, 84, 34, 97, 99, 90, 98],
    ]
    print(f'{parity(big_puzzle)=}')
    print(f'{manhattan_distance(big_puzzle)=}')
    print(f'{(parity(big_puzzle) + manhattan_distance(example_start_state)) % 2=}')
    print(is_goal(((1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12), (13, 14, 15, 0))))
    print('Solving...')
    # Solve the puzzle
    start = time.perf_counter()
    solution = slide_puzzle(example_start_state)
    stop = time.perf_counter()
    time.sleep(1)
    # Print the solution
    # visualize_solution(solution_path)
    print(f"Time = {(stop - start) * 1000:.2f} ms")
    print(f'{solution = }')
    print(f'{len(solution) = }')
