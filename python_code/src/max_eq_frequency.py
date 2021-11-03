from collections import defaultdict


class Solution:

    @staticmethod
    def max_equal_freq(nums):
        # nums as a multiset
        freq = defaultdict(int)
        for n in nums:
            freq[n] += 1
        # number of elements in nums that have a given frequency
        freq_count = defaultdict(int)
        for f in freq.values():
            freq_count[f] += 1
        i = len(nums)
        while not is_prefix(freq_count, i):
            i -= 1
            n = nums[i]
            f = freq[n]
            v = freq_count[f]
            if v == 1:
                del freq_count[f]
            else:
                freq_count[f] -= 1
            if f == 1:
                del freq[n]
            else:
                freq[n] = f - 1
                freq_count[f - 1] += 1

        return i


def is_prefix(freq_count, n):
    if freq_count[1] == n or n in freq_count:
        return True
    if len(freq_count) == 2:
        mx, mn = max(freq_count.keys()), min(freq_count.keys())
        return mn == 1 and freq_count[1] == 1 \
               or mx == mn + 1 and freq_count[mx] == 1
    return False


def largest_rectangle_in_histogram(histogram):
    res, corners = 0, [(0, 0)]
    histogram.append(0)

    for i, h in enumerate(histogram):
        j = i
        while h < corners[-1][1]:
            j, k = corners.pop()
            res = max(res, (i - j) * k)
        if h > corners[-1][1]:
            corners.append((j, h))
    return res


def largest_square_in_histogram(histogram):
    res, corners = 0, [(0, 0)]
    histogram.append(0)

    for i, h in enumerate(histogram):
        j = i
        while h < corners[-1][1]:
            j, k = corners.pop()
            res = max(res, min(i - j, k))
        if h > corners[-1][1]:
            corners.append((j, h))
    return res * res


def largest_rect_in_matrix(matrix):
    histo = [0] * len(matrix[0])
    res = 0
    for i in range(0, len(matrix)):
        histo = [h + 1 if c == 'X' else 0 for h, c in zip(histo, matrix[i])]
        res = max(res, largest_rectangle_in_histogram(histo))
    return res


if __name__ == "__main__":
    # print(Solution().maxEqualFreq([1, 2]))

    matrix = \
        """\
X___X__X_X
_XX_XX__XX
XX_XX_X_XX
XXX__XX_XX
_XXX____XX"""
    matrix = [list(row) for row in matrix.split('\n')]
    print(matrix)
    print(*matrix, sep='\n')
    print(largest_rect_in_matrix(matrix))
    print(largest_rectangle_in_histogram([2, 3, 5, 4]))

