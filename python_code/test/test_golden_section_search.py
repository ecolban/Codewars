import math
from random import uniform
from unittest import TestCase

from src.golden_section_search import gss, gss_array, DELTA


class TestGoldenSectionSearch(TestCase):

    def consume_coin(self, f):
        def wrapper(x):
            self.assertGreater(self.coins, 0, "Oh, no! You ran out of coins.")
            self.coins -= 1
            return f(x)

        return wrapper

    def test_gss_array(self):
        ar = [i + 1000 for i in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 21,
                                 20, 19, 18, 17, 16, 15, 14, 13, 10, 9, 8, 7, 6, 5, 3, 1, 0]]
        expected = 1021
        self.assertEqual(gss_array(ar), expected)

    def test_gss_1(self):

        @self.consume_coin
        def f(x):
            return x * (1 - x)

        self.coins = 30
        expected = 0.5
        self.assertAlmostEqual(gss(f), expected, delta=DELTA)

    def test_gss_2(self):

        @self.consume_coin
        def f(x):
            return -abs(x * x - 0.49)

        self.coins = 30
        expected = 0.7
        self.assertAlmostEqual(gss(f), expected, delta=DELTA)

    def test_gss_3(self):

        @self.consume_coin
        def f(x):
            return -x

        self.coins = 30
        expected = 0
        self.assertAlmostEqual(gss(f), expected, delta=DELTA)

    def test_gss_4(self):

        @self.consume_coin
        def f(x):
            return x

        self.coins = 30
        expected = 1
        self.assertAlmostEqual(gss(f), expected, delta=DELTA)

    def test_random(self):
        for _ in range(10):
            x_max = uniform(0, 1)

            @self.consume_coin
            def f(x):
                return 12.34 * (x - x_max if x < x_max else x_max - x) + 1.23

            self.coins = 29
            self.assertAlmostEqual(gss(f), x_max, delta=DELTA)

    def test_number_of_calls(self):
        phi = (math.sqrt(5) - 1) / 2
        interval_len = 1.0
        num_calls = 2  # count the 2 initial calls
        while interval_len >= 2e-6:
            interval_len *= phi  # reduce the interval length by phi per iteration
            num_calls += 1  # count one call per iteration
        expected = 30
        self.assertEqual(num_calls, expected)
