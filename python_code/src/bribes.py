from functools import lru_cache


def solve(bribes):
    if len(bribes) <= 2:
        return sum(bribes)

    @lru_cache(maxsize=None)
    def solve_h(i, j):
        if j - i <= 2:
            return sum(bribes[i:j])
        return min(max(solve_h(i, k), solve_h(k + 1, j)) + bribes[k] for k in range(i + 1, j - 1))

    return solve_h(0, len(bribes))


print([20 - i // 2 for i in range(16)])
print(solve([20 - i // 2 for i in range(16)]))
