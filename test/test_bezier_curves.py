from random import uniform
from unittest import TestCase

from bezier_curves import *


def assert_equal_points(p1, p2, delta=1e-6):
    if len(p1) != len(p2): return False
    return all(abs(a - b) < delta for (a, b) in zip(p1, p2))


class TestBezierCurves(TestCase):

    def test_initialization(self):
        line = Line(1, 2, 3, 4)
        quad = Quad(1, 2, 3, 4, 5, 6)
        cubic = Cubic(1, 2, 3, 4, 5, 6, 7, 8)

        self.assertTrue(isinstance(line, Segment))
        self.assertTrue(isinstance(line, Line))

        self.assertTrue(isinstance(quad, Segment))
        self.assertTrue(isinstance(quad, Quad))

        self.assertTrue(isinstance(cubic, Segment))
        self.assertTrue(isinstance(cubic, Cubic))

    def test_control_points(self):
        line = Line(1, 2, 3, 4)
        quad = Quad(1, 2, 3, 4, 5, 6)
        cubic = Cubic(1, 2, 3, 4, 5, 6, 7, 8)
        self.assertEqual(line.control_points, (1, 2, 3, 4))
        self.assertEqual(quad.control_points, (1, 2, 3, 4, 5, 6))
        self.assertEqual(cubic.control_points, (1, 2, 3, 4, 5, 6, 7, 8))

    def test_point_at(self):
        line = Line(0, 2.5, 3, 6.5)
        self.assertTrue(assert_equal_points(line.point_at(0.5), (1.5, 4.5)))

        quad = Quad(0, 2.5, 3, 6.5, 6, 10.5)
        self.assertTrue(assert_equal_points(quad.point_at(0.5), (3, 6.5)))

        cubic = Cubic(0, 2.5, 3, 6.5, 6, 10.5, 9, 14.5)
        self.assertTrue(assert_equal_points(cubic.point_at(0.5), (4.5, 8.5)))

    def test_sub_segment(self):
        line = Line(*(uniform(0, 10.0) for _ in range(4)))
        for _ in range(10):
            t0 = uniform(0, 1)
            sub_line = line.sub_segment(t0)
            self.assertTrue(all(assert_equal_points(line.point_at(t0 * t), sub_line.point_at(t))
                            for t in (i * 0.01 for i in range(0, 101))))

        quad = Quad(*(uniform(0, 10.0) for _ in range(6)))
        for _ in range(10):
            t0 = uniform(0, 1)
            sub_quad = quad.sub_segment(t0)
            self.assertTrue(all(assert_equal_points(quad.point_at(t0 * t), sub_quad.point_at(t))
                            for t in (i * 0.01 for i in range(0, 101))))

        cubic = Cubic(*(uniform(0, 10.0) for _ in range(8)))
        for _ in range(10):
            t0 = uniform(0, 1)
            sub_cubic = cubic.sub_segment(t0)
            self.assertTrue(all(assert_equal_points(cubic.point_at(t0 * t), sub_cubic.point_at(t))
                            for t in (i * 0.01 for i in range(0, 101))))
