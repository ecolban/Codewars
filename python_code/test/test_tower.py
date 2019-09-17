from unittest import TestCase
from src.tower import *


class TestTower(TestCase):
    def test_tower(self):
        self.assertEqual(pow(3, 27, 25), tower(3, 3, 25))
        self.assertEqual(4, tower(2, 2, 1000))
        self.assertEqual(16, tower(2, 3, 100000))
        self.assertEqual(65536, tower(2, 4, 100000000))
        self.assertEqual(256, tower(4, 2, 10000000))
        self.assertNotEqual(tower(13, 3, 31), pow(13, tower(13, 2, 31), 31))
        self.assertEqual(tower(13, 3, 31), pow(13, tower(13, 2, 30), 31))
        self.assertEqual(tower(13, 3, 31), tower(13, 2, 31))
        m = 1001
        t_3_3 = 3 ** 3 ** 3
        t_3_4 = pow(3, t_3_3, m)
        self.assertEqual(t_3_4, tower(3, 4, m))
        self.assertEqual(pow(3, t_3_3, m), tower(3, 4, m))
        t_2_4 = pow(2, 2 ** 2 ** 2)
        self.assertEqual(65536, t_2_4)
        t_2_5 = pow(2, t_2_4, 720)
        t_2_6 = pow(2, t_2_5, m)
        self.assertEqual(t_2_6, tower(2, 6, m))
        self.assertEqual(2625191611, tower(3121, 109802, 8274923478))

    def test_power_cycle(self):
        self.assertEqual((1, 30), power_cycle(4, 143))
        self.assertEqual((1, 55), power_cycle(4, 121))
        self.assertEqual((128, 62500), power_cycle(2, 10000000))
        self.assertTrue(10 ** 6 < 2 * 3 ** 14 < 10 ** 7)
        self.assertTrue(2 * 3 ** 14 < 10 ** 7 < 2 * 3 ** 15)
        self.assertEqual((3 ** 14, 1), power_cycle(3, 2 * 3 ** 14))
        self.assertEqual((4, 20), power_cycle(2, 100))
        self.assertTrue(all(totient(100) % power_cycle(n, 100)[1] == 0 for n in range(2, 100)))
        for n in range(100, 1000, 7):
            self.assertTrue(all(totient(n) % power_cycle(n, n)[1] == 0 for n in range(2, n)))

    def test_find_cycle(self):

        def f(n):
            return n % 23 * 10

        self.assertEqual((10, 22), find_cycle(f, 10))