from itertools import cycle
from random import randrange


def survivor_simulator(num_warriors):
    warriors = [True] * num_warriors  # warrior[i] == True means warrior i + 1 is alive
    indices = cycle(range(num_warriors))
    killer = 0
    for _ in range(num_warriors - 1):
        killer = next(i for i in indices if warriors[i])
        killed = next(i for i in indices if warriors[i])
        warriors[killed] = False
    return killer + 1


def survivor(num_warriors):
    p = 1
    while p <= num_warriors:
        p *= 2
    p //= 2
    return 2 * (num_warriors - p) + 1


def test_survivor():
    for p in range(10):
        assert survivor_simulator(2 ** p) == 1
        assert survivor(2 ** p) == 1
    assert survivor_simulator(100) == 73
    assert survivor(100) == 73
    for _ in range(100):
        n = randrange(10_000)
        assert survivor_simulator(n) == survivor(n)
