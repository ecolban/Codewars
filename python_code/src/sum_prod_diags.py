from functools import reduce
from operator import mul


def sum_prod_diags(matrix):
    n = len(matrix)
    sum1 = sum(reduce(mul, (row[i - k] for i, row in enumerate(matrix) if 0 <= i - k < n)) for k in range(-n + 1, n))
    sum2 = sum(reduce(mul, (row[k - i] for i, row in enumerate(matrix) if 0 <= k - i < n)) for k in range(0, 2 * n - 1))
    return sum1 - sum2


if __name__ == '__main__':
    M1 = [[1, 4, 7, 6, 5],
          [-3, 2, 8, 1, 3],
          [6, 2, 9, 7, -4],
          [1, -2, 4, -2, 6],
          [3, 2, 2, -4, 7]]
    print(sum_prod_diags(M1))
