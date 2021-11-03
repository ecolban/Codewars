from functools import reduce, cache
from itertools import product
from math import gcd

"""
## Intro

Pierre and Blaise are playing a game that has multiple rounds. They each have put $100 in a pot and whoever wins 3 
rounds first gets the pot. The winner of each round is completely random and the players have an equal probability of 
winning each round. After 3 rounds, Blaise has won two rounds and Pierre has won one round. Pierre then says he has to 
leave and is about to remove his $100 when Blaise says: "Wait a sec! I am in a better position than you to win the pot, 
so I should get a larger part of the pot. Take $50 and leave the rest for me and we can call it quits."

Pierre then starts enumerating all the possible ways that the game could unfold and discovers that, indeed, in 3 out of 
4 cases, Blaise is the winner. So he agrees with Blaise and takes his $50.

# Challenge

Assume there are `n` players who have each put the same amount in a pot. The first to win `rounds_to_win` rounds gets 
the pot. Before they complete the game, they decide to stop and divide the pot _fairly_ among each other. The number of
rounds that each player has won is given by a list `wins = [w_0, w_1, ...]` of length `n` where `wins[i]` is the number 
of rounds that player `i` has won. Write a function `divide_pot` that takes `rounds_to_win` and `wins` as arguments and 
returns a list of ints `f = [f_0, f_1, ...]` such that `Fraction(f[i], sum(f)) ` is the exact fraction of the pot that 
player `i` should receive. The entries of `f` must not have a common divisor greater than `1`.

# Input constraints

1. `2 <= n <= 10`
2. `3 <= rounds_to_win <= 100`
3. `0 <= wins[i] < rounds_to_win` for all `0 <= i < n`, 
"""


def divide_pot(num_rounds, wins):
    """Uses recursion and may result in stack overflow."""
    score = tuple(num_rounds - w for w in wins)
    num_players = len(score)

    @cache
    def h(score_):
        e = sum(score_) - num_players
        distr = [
            [num_players ** e if j == i else 0 for j in range(len(score_))] if s - 1 == 0
            else h(tuple(s_ - 1 if i == j else s_ for j, s_ in enumerate(score_)))
            for i, s in enumerate(score_)
        ]
        return [sum(a) for a in zip(*distr)]

    preliminary_result = h(score)
    d = reduce(gcd, preliminary_result)
    return [x // d for x in preliminary_result]


def matrix_get(m, t):
    """Returns m[t[0]][t[1]]...[t[-1]]"""
    for i in t:
        m = m[i]
    return m


def matrix_set(m, t, v):
    """Same effect as m[t[0]][t[1]]...[t[-1]] = v"""
    m = matrix_get(m, t[:-1])
    m[t[-1]] = v


def divide_pot2(num_rounds, wins):
    dimensions = [num_rounds - w for w in wins]
    """Builds an N-dimensional "Pascal triangle" using iteration."""
    num_dimensions = len(dimensions)

    def initialize_matrix(dims):
        return None if not dims else [initialize_matrix(dims[1:]) for _ in range(dims[0] + 1)]

    pascal = initialize_matrix(dimensions)
    for t in product(*(range(d + 1) for d in dimensions)):
        s = sum(e <= 0 for e in t)
        if s <= 1:
            v = ([num_dimensions ** (sum(t) - num_dimensions + 1) if e == 0 else 0 for e in t] if s == 1
                 else [sum(a) for a in zip(*(matrix_get(pascal, [e_ - 1 if i == j else e_ for j, e_ in enumerate(t)])
                                             for i, e in enumerate(t) if e > 0))])
            matrix_set(pascal, t, v)
    prelim_result = matrix_get(pascal, dimensions)
    d = reduce(gcd, prelim_result)
    return [e // d for e in prelim_result]
