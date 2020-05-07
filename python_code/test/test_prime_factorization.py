from unittest import TestCase

from src.prime_factorization import *


class TestPrimeFactorization(TestCase):

    def test_is_prime(self):
        self.assertTrue(is_prime(101))
        self.assertTrue(is_prime(103))
        self.assertEqual([101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163],
                         [i for i in range(101, 165, 2) if is_prime(i)])

    def test_prime_factors(self):
        self.assertEqual([(2, 1), (5, 1)], prime_factors(10))
        self.assertEqual([(2, 2), (3, 1)], prime_factors(12))
        self.assertEqual([(2, 4)], prime_factors(16))
        self.assertEqual([(2, 1), (7, 2)], prime_factors(98))
        self.assertEqual([(2, 6), (3, 4), (5, 2), (107, 1)], prime_factors(2 ** 6 * 3 ** 4 * 5 ** 2 * 107))
        self.assertEqual([(3119, 1), (4261, 1)], prime_factors(13290059))

    def test_totient(self):
        self.assertEqual(12, totient(36))
        self.assertEqual(40, totient(100))
        self.assertEqual(1000, totient(11 * 101))
        self.assertEqual(2 ** 5 * 3 ** 3 * 2 * 5 * 4 * 106, totient(2 ** 6 * 3 ** 4 * 5 ** 2 * 107))

    def test_largest_prime_factor(self):
        self.assertEqual(101, largest_prime_factor(101 * 17 * 5))
        self.assertRaises(ValueError, largest_prime_factor, 1)

    def test_smallest_prime_factor(self):
        self.assertEqual(5, smallest_prime_factor(101 * 17 * 5))
        self.assertRaises(StopIteration, smallest_prime_factor, 1)

    def test_divisors(self):
        self.assertEqual([1, 2003], divisors(2003))
        self.assertEqual(2, divisor_count(2003))
        self.assertEqual([1, 17, 101, 101 * 17], divisors(101 * 17))
        self.assertEqual(4, divisor_count(101 * 17))
        self.assertEqual([7 ** i for i in range(5)], divisors(7 ** 4))
        self.assertEqual(5, divisor_count(7 ** 4))
        self.assertEqual(sorted([7 ** i * 13 ** j for i, j in product(range(5), range(3))]), divisors(7 ** 4 * 13 ** 2))
        self.assertEqual(15, divisor_count(7 ** 4 * 13 ** 2))
