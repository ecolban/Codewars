from collections import defaultdict
from itertools import combinations
from math import gcd
from random import randrange

"""\
<?xml version="1.0" encoding="UTF-8"?><!--Created with Drawmetry (http://www.drawmetry.com/)--><svg xmlns="http://www.w3.org/2000/svg" width="34.00" height="34.00" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:dm="http://www.drawmetry.com">
  <defs/>
  <g transform="translate(2.00, 2.00)">
    <line id="L_0" x1="10.0000" y1="15.0000" x2="20.0000" y2="15.0000" stroke="#000000" stroke-width="1.0"/>
    <line id="L_1" x1="15.0000" y1="10.0000" x2="15.0000" y2="20.0000" stroke="#000000" stroke-width="1.0"/>
    <dm:point id="P_0" x="15.0000" y="15.0000" visible="true"/>
    <dm:point id="P_1" x="10.0000" y="15.0000" visible="false"/>
    <dm:point id="P_2" x="20.0000" y="15.0000" visible="false"/>
    <dm:point id="P_3" x="15.0000" y="10.0000" visible="false"/>
    <dm:point id="P_4" x="15.0000" y="20.0000" visible="false"/>
  </g>
  <dm:constraint dm:target="P_1" dm:constraint-text="=horizontal(P_0) and hdistance(P_0, -5.0)"/>
  <dm:constraint dm:target="P_2" dm:constraint-text="=horizontal(P_0) and hdistance(P_0,5.0)"/>
  <dm:constraint dm:target="P_3" dm:constraint-text="=vertical(P_0) and vdistance(P_0,5.0)"/>
  <dm:constraint dm:target="P_4" dm:constraint-text="=vertical(P_0) and vdistance(P_0, -5.0)"/>
  <dm:constraint dm:target="L_0" dm:constraint-text="=vertices(P_1, P_2)"/>
  <dm:constraint dm:target="L_1" dm:constraint-text="=vertices(P_3, P_4)"/>
</svg>
"""


def svg_gen(pts):
    yield """\
<?xml version="1.0" encoding="UTF-8"?>
<!--Created with Drawmetry (http://www.drawmetry.com/)-->
<svg xmlns="http://www.w3.org/2000/svg" width="34.00" height="34.00" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:dm="http://www.drawmetry.com">
  <defs/>
  <g transform="translate(2.00, 2.00)">"""
    for i, (x, y) in enumerate(pts):
        yield f'    <line id="L_{2 * i}" x1="{x * 40 + 10}.0" y1="{y * 40 + 15}.0" x2="{x * 40 + 20}.0" y2="{y * 40 + 15}.0" stroke="#000000" stroke-width="1.0"/>'
        yield f'    <line id="L_{2 * i + 1}" x1="{x * 40 + 15}.0" y1="{y * 40 + 10}.0" x2="{x * 40 + 15}.0" y2="{y * 40 + 20}.0" stroke="#000000" stroke-width="1.0"/>'
    for i, (x, y) in enumerate(pts):
        yield f'    <dm:point id="P_{5 * i + 0}" x="{x * 40 + 15}.0" y="{y * 40 + 15}.0" visible="true"/>'
        yield f'    <dm:point id="P_{5 * i + 1}" x="{x * 40 + 10}.0" y="{y * 40 + 15}.0" visible="false"/>'
        yield f'    <dm:point id="P_{5 * i + 2}" x="{x * 40 + 20}.0" y="{y * 40 + 15}.0" visible="false"/>'
        yield f'    <dm:point id="P_{5 * i + 3}" x="{x * 40 + 15}.0" y="{y * 40 + 10}.0" visible="false"/>'
        yield f'    <dm:point id="P_{5 * i + 4}" x="{x * 40 + 15}.0" y="{y * 40 + 20}.0" visible="false"/>'
    yield "  </g>"
    for i, (x, y) in enumerate(pts):
        yield f'  <dm:constraint dm:target="P_{5 * i + 1}" dm:constraint-text="=horizontal(P_{5 * i}) and hdistance(P_{5 * i}, -5.0)"/>'
        yield f'  <dm:constraint dm:target="P_{5 * i + 2}" dm:constraint-text="=horizontal(P_{5 * i}) and hdistance(P_{5 * i},5.0)"/>'
        yield f'  <dm:constraint dm:target="P_{5 * i + 3}" dm:constraint-text="=vertical(P_{5 * i}) and vdistance(P_{5 * i},5.0)"/>'
        yield f'  <dm:constraint dm:target="P_{5 * i + 4}" dm:constraint-text="=vertical(P_{5 * i}) and vdistance(P_{5 * i}, -5.0)"/>'
        yield f'  <dm:constraint dm:target="L_{2 * i}" dm:constraint-text="=vertices(P_{5 * i + 1}, P_{5 * i + 2})"/>'
        yield f'  <dm:constraint dm:target="L_{2 * i + 1}" dm:constraint-text="=vertices(P_{5 * i + 3}, P_{5 * i + 4})"/>'
    yield '</svg>'


def count_rect_triang(points):
    points = set((x, y) for [x, y] in points)
    d = defaultdict(lambda: defaultdict(int))
    for p1 in points:
        for p2 in points:
            if p1 != p2:
                d[p1][direction(p1, p2)] += 1
    return sum(d[p][(a, b)] * d[p][(-b, a)] for p in points for (a, b) in d[p] if a > 0 and (-b, a) in d[p])


def direction(p1, p2):
    a, b = p1[0] - p2[0], p1[1] - p2[1]
    if a == 0: return 0, 1
    if b == 0: return 1, 0
    if b < 0: a, b = -a, -b
    c = gcd(a, b)
    return a // c, b // c


# ------------------------------------
# Following is the solution that got the most "Best Practice" votes.
# -------------------------------------------------

def isRect(a, b, c):
    X, Y, Z = sorted(sum((q - p) ** 2 for p, q in zip(p1, p2)) for p1, p2 in [(a, b), (a, c), (b, c)])
    return X + Y == Z


def count_rect_triang_(points):
    return sum(isRect(*c) for c in combinations(set(map(tuple, points)), 3))


if __name__ == "__main__":
    m, n = 20, 50
    pts = []
    for y in range(m):
        for x in range(n):
            if randrange(10) < 2:
                pts.append((x, y))
                print('. ', end='')
            else:
                print('  ', end='')
        print()

    print(f'\n{m}x{n}: {count_rect_triang_(pts)}')

    with open("grid.svg", mode="w") as f:
        for line in svg_gen(pts):
            f.write(line)
            f.write('\n')
    # print(f'\n{n}x{2 * n}: {count_rect_triang_(pts)}')
