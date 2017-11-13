from unittest import TestCase
from survivors import survivor, survivor1, nth_survivor
from random import randrange


class TestSurvivor(TestCase):
    def test_survivor(self):
        self.assertEqual([i for i in range(1, 100) if survivor(i)], [1, 3, 7, 13, 19, 27, 39, 49, 63, 79, 91])
        self.assertEqual(survivor(3903), False)
        self.assertEqual(survivor(13903), True)
        self.assertEqual(survivor(99998653), True)

    def test_survivor1(self):
        self.assertEqual([i for i in range(1, 100) if survivor1(i)], [1, 3, 7, 13, 19, 27, 39, 49, 63, 79, 91])
        self.assertEqual(survivor1(3903), False)
        self.assertEqual(survivor1(13903), True)
        # self.assertEqual(survivor1(99998653), True) #Results in stack overflow
        for _ in range(10000):
            n = randrange(1, 100000, 2)
            self.assertEqual(survivor(n), survivor1(n))


def test_nth_survivor(self):
    self.assertEqual(nth_survivor(133), 13903)
    self.assertEqual(nth_survivor(9678), 73560949)
    self.assertEqual(nth_survivor(11284), 99998653)
