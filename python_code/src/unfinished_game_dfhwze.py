from fractions import Fraction
from functools import cache, lru_cache
from math import gcd, lcm

fac = cache(lambda n: 1 if n < 2 else n * fac(n - 1))
nCk = cache(lambda n, k: fac(n) // (fac(k) * fac(n - k)))


def convert_to_integers(ratios, common_factor=1, common_divisor=0):
    for ratio in ratios:
        common_factor = lcm(common_factor, ratio.denominator)
    res = [ratio.numerator * common_factor // ratio.denominator for ratio in ratios]
    for integer in res:
        common_divisor = gcd(common_divisor, integer)
    return [integere // common_divisor for integere in res]


@lru_cache(maxsize=None)
def partition(opponents, rem_rounds):
    res = Fraction(0, 1)
    if (not opponents): return 0 if rem_rounds > 0 else 1
    opponent, *others = opponents
    if (not others) and rem_rounds >= opponent: return 0
    if rem_rounds == 0: return 1

    allowed_wins = opponent - 1
    min_rounds = max(0, rem_rounds - (sum(others) - len(others))) if others else rem_rounds
    max_rounds = min(allowed_wins, rem_rounds)
    if min_rounds > max_rounds: return 0

    for rounds in range(min_rounds, max_rounds + 1):
        num_arrangements = nCk(rem_rounds, rounds)
        next_partition = partition(tuple(others), rem_rounds - rounds)
        res += num_arrangements * next_partition

    return res


def divide_pot(num_rounds, wins):
    num_players = len(wins)
    remaining_wins = [num_rounds - win for win in wins]
    assert all(remaining_win > 0 for remaining_win in remaining_wins), "should have no winner yet"

    ans = [Fraction(0, 1) for _ in range(num_players)]
    max_rounds = sum(remaining_wins) - num_players + 1
    p = Fraction(1, num_players)

    for player in range(num_players):
        min_rounds = remaining_wins[player]
        for rounds in range(min_rounds, max_rounds + 1):
            p_arrangement = p ** rounds
            num_arrangements = nCk(rounds - 1, remaining_wins[player] - 1)
            opponents = tuple(sorted([remaining_wins[i] for i in range(num_players) if i != player]))
            rest = partition(opponents, rounds - remaining_wins[player])
            ans[player] += p_arrangement * num_arrangements * rest

    return convert_to_integers(ans)