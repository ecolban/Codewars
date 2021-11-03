from functools import lru_cache


def solve(bribes):

    @lru_cache(maxsize=None)
    def solve_h(i, j):
        if j - i <= 2:
            return sum(bribes[i:j])
        return min(max(solve_h(i, k), solve_h(k + 1, j)) + bribes[k] for k in range(i + 1, j - 1))

    return solve_h(0, len(bribes))


if __name__ == '__main__':
    bribes = [20 - i // 2 for i in range(16)]
    print(bribes)
    print(solve(bribes))
    print(solve(bribes[1:4]))
    print(solve(bribes[7:]))
    print(solve(bribes[:0]))
