from unittest import TestCase
from prime_factorization import *


class TestPrimeFactorization(TestCase):

    def test_is_prime(self):
        self.assertTrue(is_prime(101))
        self.assertTrue(is_prime(103))
        self.assertEqual([101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163],
                         [i for i in range(101, 165, 2) if is_prime(i)])

    def test_gen_prime_factors(self):
        self.assertEqual([7], list(gen_prime_factors(7)))
        self.assertEqual([7, 11, 13], list(gen_prime_factors(1001)))
        n = 2 * 2 * 2 * 7 * 7 * 11 * 13
        self.assertEqual([2, 2, 2, 7, 7, 11, 13], list(gen_prime_factors(n)))
        self.assertEqual({2: 3, 7: 2, 11: 1, 13: 1}, Counter(gen_prime_factors(n)))

    def test_gen_distinct_prime_factors(self):
        self.assertEqual([2, 7, 11, 13], list(gen_distinct_prime_factors(2 * 2 * 2 * 7 * 7 * 11 * 13)))

    def test_prime_factors(self):
        self.assertEqual({2: 1, 5: 1}, prime_factors(10))
        self.assertEqual({2: 2, 3: 1}, prime_factors(12))
        self.assertEqual({2: 4}, prime_factors(16))
        self.assertEqual({2: 1, 7: 2}, prime_factors(98))
        self.assertEqual({2: 6, 3: 4, 5: 2, 107: 1}, prime_factors(2 ** 6 * 3 ** 4 * 5 ** 2 * 107))

    def test_gcd(self):
        self.assertEqual(3, gcd(3 * 12, 3 * 17))
        self.assertEqual(6, gcd(6, 0))
        self.assertEqual(6, gcd(0, 6))
        self.assertEqual(1, gcd(1, 6))
        self.assertEqual(1, gcd(6, 1))
        self.assertEqual(12, gcd(12, 12 * 12))
        for m in range(1, 100):
            for n in range(m):
                self.assertEqual(gcd(m, n), gcd(n,m))
                self.assertEqual(m % gcd(m, n), 0)
                self.assertEqual(n % gcd(m, n), 0)

    def test_totient(self):
        self.assertEqual(12, totient(36))
        self.assertEqual(40, totient(100))
        self.assertEqual(1000, totient(11 * 101))
        self.assertEqual(2 ** 5 * 3 ** 3 * 2 * 5 * 4 * 106, totient(2 ** 6 * 3 ** 4 * 5 ** 2 * 107))

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
        self.assertTrue(10**6 < 2 * 3**14 < 10**7)
        self.assertTrue(2 * 3**14 < 10**7 < 2 * 3**15)
        self.assertEqual((3**14, 1), power_cycle(3, 2 * 3**14))
        self.assertEqual((4, 20), power_cycle(2, 100))
        self.assertTrue(all(totient(100) % power_cycle(n, 100)[1] == 0 for n in range(2, 100)))
        for n in range(100, 1000, 7):
            self.assertTrue(all(totient(n) % power_cycle(n, n)[1] == 0 for n in range(2, n)))
