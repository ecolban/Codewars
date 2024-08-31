from collections import Counter
from functools import reduce, cache
from itertools import product
from math import factorial, gcd, prod

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


def divide_pot1(num_rounds, wins):
    score = tuple(num_rounds - w for w in wins)
    num_players = len(score)

    @cache
    def h(score_: tuple[int, ...]) -> int:
        """Returns the part of the pot that player with score_[0] should receive."""
        denominator = num_players ** (sum(score_) - num_players)
        return sum(
            (denominator if i == 0 else 0) if s == 1
            else h(tuple(s_ - 1 if i == j else s_ for j, s_ in enumerate(score_)))
            for i, s in enumerate(score_)
        )

    def swap(k):
        return tuple(score[k] if i == 0 else score[0] if i == k else s
                     for i, s in enumerate(score))

    preliminary_result = [h(swap(k)) for k in range(len(score))]
    d = gcd(*preliminary_result)
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
        denominator = num_dimensions ** (sum(t) - num_dimensions + 1)
        if s == 1:
            v = [denominator if e == 0 else 0 for e in t]
            matrix_set(pascal, t, v)
        elif s == 0:
            v = [sum(a) for a in zip(*(matrix_get(pascal, [e_ - 1 if i == j else e_ for j, e_ in enumerate(t)])
                                       for i, e in enumerate(t)))]
            matrix_set(pascal, t, v)
    prelim_result = matrix_get(pascal, dimensions)
    d = reduce(gcd, prelim_result)
    return [e // d for e in prelim_result]


def divide_pot3(num_rounds, wins):
    dimensions = [num_rounds - w for w in wins]
    """Builds an N-dimensional "Pascal triangle" using iteration."""
    num_dimensions = len(dimensions)
    max_dimension = max(dimensions)

    def initialize_matrix(num_d):
        return 0 if num_d == 0 else [initialize_matrix(num_d - 1) for _ in range(max_dimension + 1)]

    pascal = initialize_matrix(num_dimensions)
    for t in product(*(range(max_dimension + 1) for _ in dimensions)):
        s = sum(e <= 0 for e in t)
        denominator = num_dimensions ** (sum(t) - num_dimensions + 1)
        if s == 1 and t[0] == 0:
            v = denominator
            matrix_set(pascal, t, v)
        elif s == 0:
            v = sum(matrix_get(pascal, [e_ - 1 if i == j else e_ for j, e_ in enumerate(t)])
                    for i, e in enumerate(t))
            matrix_set(pascal, t, v)

    def swap(i):
        dimensions[0], dimensions[i] = dimensions[i], dimensions[0]
        return dimensions

    prelim_result = [matrix_get(pascal, swap(i)) for i in range(num_dimensions)]
    d = reduce(gcd, prelim_result)
    return [e // d for e in prelim_result]


def multinomial(*ks: int) -> int:
    return factorial(sum(ks)) // prod(map(factorial, ks))


def multiplicity(bounds):
    # We could do better, but this suffices for now
    return Counter(
        tuple(sorted(t)) for t in product(*map(range, bounds))
    )


def divide_pot4(num_rounds, wins):
    score = [num_rounds - win for win in wins]
    num_players = len(score)

    def player_0_part(score_: tuple[int, ...]) -> int:
        player_0, *others = score_

        def h1(*t: int):
            return multinomial(*t) * num_players ** (sum(score) - sum(t))

        return sum(h1(player_0 - 1, *t) * m for t, m in multiplicity(others).items())

    def swap(k: int) -> tuple[int, ...]:
        return tuple(score[k] if i == 0 else score[0] if i == k else s for i, s in enumerate(score))

    preliminary_result = [player_0_part(swap(k)) for k in range(len(score))]
    d = gcd(*preliminary_result)
    return [x // d for x in preliminary_result]
