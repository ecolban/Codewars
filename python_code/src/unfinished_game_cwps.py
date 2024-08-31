from math import gcd
from functools import lru_cache
from fractions import Fraction
from math import prod


@lru_cache(None)
def win_prob(wins, rounds_to_win):
    n = len(wins)
    if max(wins) >= rounds_to_win:
        return [1 if wins[i] >= rounds_to_win else 0 for i in range(n)]

    total_prob = [Fraction(0) for _ in range(n)]

    remaining_players = [i for i, w in enumerate(wins) if w < rounds_to_win]
    total_remaining = len(remaining_players)

    for i in remaining_players:
        new_wins = list(wins)
        new_wins[i] += 1
        next_probs = win_prob(tuple(new_wins), rounds_to_win)
        for j in range(n):
            total_prob[j] += next_probs[j] * Fraction(1, total_remaining)

    return total_prob


def divide_pot_cwps(rounds_to_win, wins):
    wins = tuple(wins)
    probs = win_prob(wins, rounds_to_win)

    denom = [prob.denominator for prob in probs]
    lcm = prod(denom) // gcd(*denom)

    shares = [prob.numerator * (lcm // prob.denominator) for prob in probs]

    return [share // gcd(*shares) for share in shares]