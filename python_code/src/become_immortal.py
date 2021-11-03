def brute_force(rows, cols, loss, m):
    s = 0
    for i in range(rows):
        for j in range(cols):
            s += max((i ^ j) - loss, 0)
    return s % m


def pow2(n):
    p = 1
    while p <= n: p <<= 1
    return p >> 1


def mult(a, b, m):
    return (a % m) * (b % m) % m


def arithmetic_sum(end, modulus, start=0, adj=0):
    """Return sum(max(i + adj, 0) for i in range(start, end)) % modulus"""
    start, end = max(0, start + adj), end + adj
    if end <= start: return 0
    # 0 <= start < end. Return (start + end - 1) * (end - start) // 2 % modulus
    k, n = start + end - 1, end - start
    return mult(k, n >> 1, modulus) if k & 1 else mult(k >> 1, n, modulus)


def elder_age(rows, cols, loss, m):
    if rows > cols: rows, cols = cols, rows
    if rows == 0: return 0
    pr, pc = pow2(rows), pow2(cols)
    row_sum = arithmetic_sum(end=pc, adj=-loss, modulus=m)
    return (mult(row_sum, rows, m)
            + elder_age(cols - pc, rows, loss - pc, m)
            if rows < pc else
            mult(row_sum, pr, m)
            + elder_age(rows - pr, pc, loss - pr, m)
            + elder_age(cols - pc, pr, loss - pc, m)
            + elder_age(rows - pr, cols - pc, loss, m)) % m


def print_matrix(rows, cols, loss):
    for row in range(rows):
        print('|' + '|'.join(f'{max((row ^ col) - loss, 0):2d}' for col in range(cols)) + '|')


if __name__ == '__main__':
    print_matrix(15, 24, 0)
    print('|' + '=' * 71 + '|')
    print_matrix(15, 24, 2)
    res = elder_age(15, 24, 2, 100)
    print(res)
    res = brute_force(15, 24, 2, 100)
    print(res)
