Given a set of points on a quadratic grid, count the rectangles whose vertices are all in the given set. 

The points are given as an indexable list of coordinate pairs, but the exact representation is language dependent. The coordinates are non-negative integers (0 inclusive) bounded by 100. The axes of the coordinate system are orthogonal and equally scaled.
The sides of a rectangle need not be horizontal or vertical. Recall that a rectangle is a quadrilateral where all angles are right (90 degrees), but there are other equivalent characterizations which may be more useful for solving this kata.
**Example 1:**
Given the points 
```
[(0, 0), (0, 1), (0, 2),
 (1, 0), (1, 1), (1, 2),
 (2, 0), (2, 1), (2, 2)]
```
There a 10 rectangles whose vertices are in this list. Nine rectagles have their sides aligned with the axes of the coordinate system, and the last rectangle is the one with coordinates `(0, 1), (1, 0), (2, 1), (1, 2)`:
![svg image](data:image/svg+xml,%3C%3Fxml%20version%3D%221.0%22%20encoding%3D%22UTF-8%22%3F%3E%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20width%3D%22100%22%20height%3D%22100%22%20xmlns%3Axlink%3D%22http%3A//www.w3.org/1999/xlink%22%3E%3Cpolygon%20stroke%3D%22none%22%20fill%3D%22%23ffffff%22%20points%3D%220%200%200%20100%20100%20100%2C%20100%2C%200%22/%3E%3Cpolygon%20stroke%3D%22%23999999%22%20fill%3D%22none%22%20points%3D%2210%2050%2010%2010%2050%2010%2050%2050%22/%3E%3Cpolygon%20stroke%3D%22%23999999%22%20fill%3D%22none%22%20points%3D%2210%2090%2010%2010%2050%2010%2050%2090%22/%3E%3Cpolygon%20stroke%3D%22%23999999%22%20fill%3D%22none%22%20points%3D%2210%2010%2010%2050%2090%2050%2090%2010%22/%3E%3Cpolygon%20stroke%3D%22%23999999%22%20fill%3D%22none%22%20points%3D%2210%2010%2010%2090%2090%2090%2090%2010%22/%3E%3Cpolygon%20stroke%3D%22%23999999%22%20fill%3D%22none%22%20points%3D%2210%2050%2010%2090%2050%2090%2050%2050%22/%3E%3Cpolygon%20stroke%3D%22%23999999%22%20fill%3D%22none%22%20points%3D%2250%2010%2010%2050%2050%2090%2090%2050%22/%3E%3Cpolygon%20stroke%3D%22%23999999%22%20fill%3D%22none%22%20points%3D%2210%2090%2010%2050%2090%2050%2090%2090%22/%3E%3Cpolygon%20stroke%3D%22%23999999%22%20fill%3D%22none%22%20points%3D%2250%2050%2050%2010%2090%2010%2090%2050%22/%3E%3Cpolygon%20stroke%3D%22%23999999%22%20fill%3D%22none%22%20points%3D%2250%2090%2050%2010%2090%2010%2090%2090%22/%3E%3Cpolygon%20stroke%3D%22%23999999%22%20fill%3D%22none%22%20points%3D%2250%2050%2050%2090%2090%2090%2090%2050%22/%3E%3Ccircle%20cx%3D%2210%22%20cy%3D%2210%22%20r%3D%222%22%20stroke%3D%22%23000000%22/%3E%3Ccircle%20cx%3D%2210%22%20cy%3D%2250%22%20r%3D%222%22%20stroke%3D%22%23000000%22/%3E%3Ccircle%20cx%3D%2210%22%20cy%3D%2290%22%20r%3D%222%22%20stroke%3D%22%23000000%22/%3E%3Ccircle%20cx%3D%2250%22%20cy%3D%2210%22%20r%3D%222%22%20stroke%3D%22%23000000%22/%3E%3Ccircle%20cx%3D%2250%22%20cy%3D%2250%22%20r%3D%222%22%20stroke%3D%22%23000000%22/%3E%3Ccircle%20cx%3D%2250%22%20cy%3D%2290%22%20r%3D%222%22%20stroke%3D%22%23000000%22/%3E%3Ccircle%20cx%3D%2290%22%20cy%3D%2210%22%20r%3D%222%22%20stroke%3D%22%23000000%22/%3E%3Ccircle%20cx%3D%2290%22%20cy%3D%2250%22%20r%3D%222%22%20stroke%3D%22%23000000%22/%3E%3Ccircle%20cx%3D%2290%22%20cy%3D%2290%22%20r%3D%222%22%20stroke%3D%22%23000000%22/%3E%3C/svg%3E)
**Example 2:**
Given the points
```
[(1, 0), (4, 0),
 (1, 1), (3, 1), (9, 1),
 (0, 2), (4, 2), (5, 2), (6, 2), (9, 2),
 (2, 3), (5, 3), 
 (1, 4), (2, 4), (4, 4), (5, 4), (9, 4)]
```
There are 12 rectangles whose vertices are in the given list, as shown in the figure:
![svg image](data:image/svg+xml,%3C%3Fxml%20version%3D%221.0%22%20encoding%3D%22UTF-8%22%3F%3E%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20width%3D%22420%22%20height%3D%22180%22%20xmlns%3Axlink%3D%22http%3A//www.w3.org/1999/xlink%22%3E%3Cpolygon%20stroke%3D%22none%22%20fill%3D%22%23ffffff%22%20points%3D%220%200%200%20220%20420%20220%2C%20420%2C%200%22/%3E%3Cpolygon%20stroke%3D%22%23999999%22%20fill%3D%22none%22%20points%3D%22130%2050%2050%2010%2010%2090%2090%20130%22/%3E%3Cpolygon%20stroke%3D%22%23999999%22%20fill%3D%22none%22%20points%3D%2210%2090%2050%2010%20210%2090%20170%20170%22/%3E%3Cpolygon%20stroke%3D%22%23999999%22%20fill%3D%22none%22%20points%3D%2210%2090%20170%2010%20210%2090%2050%20170%22/%3E%3Cpolygon%20stroke%3D%22%23999999%22%20fill%3D%22none%22%20points%3D%2250%2010%20170%2010%20170%20170%2050%20170%22/%3E%3Cpolygon%20stroke%3D%22%23999999%22%20fill%3D%22none%22%20points%3D%22170%2010%20130%2050%20210%20130%20250%2090%22/%3E%3Cpolygon%20stroke%3D%22%23999999%22%20fill%3D%22none%22%20points%3D%22170%2010%2050%2050%2090%20170%20210%20130%22/%3E%3Cpolygon%20stroke%3D%22%23999999%22%20fill%3D%22none%22%20points%3D%2250%2050%20370%2050%20370%20170%2050%20170%22/%3E%3Cpolygon%20stroke%3D%22%23999999%22%20fill%3D%22none%22%20points%3D%22130%2050%20210%2090%20170%20170%2090%20130%22/%3E%3Cpolygon%20stroke%3D%22%23999999%22%20fill%3D%22none%22%20points%3D%22170%2090%20210%2090%20210%20170%20170%20170%22/%3E%3Cpolygon%20stroke%3D%22%23999999%22%20fill%3D%22none%22%20points%3D%22170%2090%20370%2090%20370%20170%20170%20170%22/%3E%3Cpolygon%20stroke%3D%22%23999999%22%20fill%3D%22none%22%20points%3D%22210%2090%20370%2090%20370%20170%20210%20170%22/%3E%3Cpolygon%20stroke%3D%22%23999999%22%20fill%3D%22none%22%20points%3D%22210%20130%2090%20130%2090%20170%20210%20170%22/%3E%3Ccircle%20cx%3D%2250%22%20cy%3D%2210%22%20r%3D%222%22%20stroke%3D%22%23000000%22/%3E%3Ccircle%20cx%3D%22170%22%20cy%3D%2210%22%20r%3D%222%22%20stroke%3D%22%23000000%22/%3E%3Ccircle%20cx%3D%2250%22%20cy%3D%2250%22%20r%3D%222%22%20stroke%3D%22%23000000%22/%3E%3Ccircle%20cx%3D%22130%22%20cy%3D%2250%22%20r%3D%222%22%20stroke%3D%22%23000000%22/%3E%3Ccircle%20cx%3D%22370%22%20cy%3D%2250%22%20r%3D%222%22%20stroke%3D%22%23000000%22/%3E%3Ccircle%20cx%3D%2210%22%20cy%3D%2290%22%20r%3D%222%22%20stroke%3D%22%23000000%22/%3E%3Ccircle%20cx%3D%22170%22%20cy%3D%2290%22%20r%3D%222%22%20stroke%3D%22%23000000%22/%3E%3Ccircle%20cx%3D%22210%22%20cy%3D%2290%22%20r%3D%222%22%20stroke%3D%22%23000000%22/%3E%3Ccircle%20cx%3D%22250%22%20cy%3D%2290%22%20r%3D%222%22%20stroke%3D%22%23000000%22/%3E%3Ccircle%20cx%3D%22370%22%20cy%3D%2290%22%20r%3D%222%22%20stroke%3D%22%23000000%22/%3E%3Ccircle%20cx%3D%2290%22%20cy%3D%22130%22%20r%3D%222%22%20stroke%3D%22%23000000%22/%3E%3Ccircle%20cx%3D%22210%22%20cy%3D%22130%22%20r%3D%222%22%20stroke%3D%22%23000000%22/%3E%3Ccircle%20cx%3D%2250%22%20cy%3D%22170%22%20r%3D%222%22%20stroke%3D%22%23000000%22/%3E%3Ccircle%20cx%3D%2290%22%20cy%3D%22170%22%20r%3D%222%22%20stroke%3D%22%23000000%22/%3E%3Ccircle%20cx%3D%22170%22%20cy%3D%22170%22%20r%3D%222%22%20stroke%3D%22%23000000%22/%3E%3Ccircle%20cx%3D%22210%22%20cy%3D%22170%22%20r%3D%222%22%20stroke%3D%22%23000000%22/%3E%3Ccircle%20cx%3D%22370%22%20cy%3D%22170%22%20r%3D%222%22%20stroke%3D%22%23000000%22/%3E%3C/svg%3E)
The vertices of these rectangles are:
```
((3, 1), (1, 0), (0, 2), (2, 3))
((0, 2), (1, 0), (5, 2), (4, 4))
((0, 2), (4, 0), (5, 2), (1, 4))
((1, 0), (4, 0), (4, 4), (1, 4))
((4, 0), (3, 1), (5, 3), (6, 2))
((4, 0), (1, 1), (2, 4), (5, 3))
((1, 1), (9, 1), (9, 4), (1, 4))
((3, 1), (5, 2), (4, 4), (2, 3))
((4, 2), (5, 2), (5, 4), (4, 4))
((4, 2), (9, 2), (9, 4), (4, 4))
((5, 2), (9, 2), (9, 4), (5, 4))
((5, 3), (2, 3), (2, 4), (5, 4))
```
The most complex tests will randomly select approximately 15% of the points in a 50-by-100 grid. The result will typically be in the thousands.

Languages/Python/Complete Solution
from collections import Counter
from itertools import combinations
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
