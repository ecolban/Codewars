from collections import Counter, defaultdict
from itertools import combinations, groupby
from random import randrange


def count_rects(points):
    """
    Returns the number of rectangles that have their vertices on a given list of points.
    The given points have integer coordinates.
    The solution is based on:
    A quadrilateral is a rectangle if and only if the diagonals have the same length and
    intersect in their respective midpoints.
    So, counting reactangles amounts to counting pairs of diagonals that have the same length
    and midpoint.
    """
    ctr = Counter(((x1 - x2) ** 2 + (y1 - y2) ** 2, x1 + x2, y1 + y2)
                  for (x1, y1), (x2, y2) in combinations(points, 2))
    return sum(m * (m - 1) // 2 for m in ctr.values() if m > 1)


def get_rects(points):
    d = defaultdict(set)
    for (x1, y1), (x2, y2) in combinations(points, 2):
        d[((x1 - x2) ** 2 + (y1 - y2) ** 2, x1 + x2, y1 + y2)].add((x1, y1, x2, y2))
    return ((x1, y1, x2, y2, x3, y3, x4, y4)
            for v in d.values() if len(v) > 1
            for (x1, y1, x3, y3), (x2, y2, x4, y4) in combinations(v, 2))

# One line solution:
# from collections import Counter as A
# from itertools import combinations as B
#
# count_rects = lambda H:sum(G*(G-1)//2for G in A(((C-D)**2+(E-F)**2,C+D,E+F)for(C,E),(D,F)in B(H,2)).values())


def int_sqrt(d2):
    return int(d2 ** 0.5)


def main(rows, cols):
    pts = [(c, r) for r in range(rows) for c in range(cols) if randrange(10) < 2]
    make_svg(pts, file='grid.svg')


def make_svg(pts, file):
    rows = max(y for x, y in pts) + 1
    cols = max(x for x, y in pts) + 1
    margin, unit = 10, 40
    width, height = 2 * margin + (cols - 1) * unit, 2 * margin + (rows - 1) * unit
    print(width, height)
    with open(file, 'w') as f:
        print('''<?xml version="1.0" encoding="UTF-8"?>''', file=f)
        print(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"'
              f' xmlns:xlink="http://www.w3.org/1999/xlink">', file=f)
        print(f'<polygon stroke="#000000" fill="#ffffff" points="0 0 0 {height} {width} {height}, {width}, 0"/>', file=f)
        for x1, y1, x2, y2, x3, y3, x4, y4 in get_rects(pts):
            print(((x1, y1), (x2, y2), (x3, y3), (x4, y4)))
            print(f'<polygon stroke="#999999" fill="none" points='
                  f'"{margin + x1 * unit} {margin + y1 * unit} '
                  f'{margin + x2 * unit} {margin + y2 * unit} '
                  f'{margin + x3 * unit} {margin + y3 * unit} '
                  f'{margin + x4 * unit} {margin + y4 * unit}"/>', file=f)
        for x, y in pts:
            print(f'''<circle cx="{margin + x * unit}" cy="{margin + y * unit}" r="2" stroke="#000000"/>''', file=f)
        print('</svg>', file=f)


def gcd(a, b):
    return gcd(b, a % b) if b > 0 else a


def count_points(r2, odd=0):
    ps = []
    for x in range(odd, int((r2/2)**0.5) + 1, 2):
        y = int((r2 - x * x)**0.5)
        if x * x + y * y == r2:
            ps.append((x, y))
    return ps


if __name__ == "__main__":
    main(10, 30)




# Given two points p1 = (x1, y1) and p2 = (x2, y2) on an m x n quadratic grid.
# Write a function that returns the set of points on the grid that lie on the circle
# with diameter p1, p2.

