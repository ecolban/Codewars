def square_sums_row(n):
    sqrs = {i * i for i in range(2, int((2 * n) ** 0.5) + 1)}
    succs = {i: [s - i for s in sqrs if i != s - i and 1 <= s - i <= n] for i in range(1, n + 1)}
    row = list()

    def helper(start):
        row.append(start)
        if len(row) == n:
            yield row.copy()
        else:
            for k in succs[row[-1]]:
                if k not in row:
                    yield from helper(k)
        row.pop(-1)

    return next((r for i in range(1, n) for r in helper(i)), False)


if __name__ == '__main__':
    row = square_sums_row(48)

    print(row)

# 100, 50, 25, 76, 38, 19, 58, 29, 88, 44, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1
# a + b / a = a / b
# ab + b^2 = a^2
# a^2 - ba + b^2 = 0
# a = (b + sqrt(b^2 - 4b^2)) / 2 = b(1 + sqrt(5))/2
# x + y = 1, xy = -1 => x^2 - x -1 = 0 => (1 +/-sqrt(5))/2 => x = 1.618, y = -0.618
