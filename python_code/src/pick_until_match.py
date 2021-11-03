from collections import defaultdict
from functools import lru_cache, reduce
from math import gcd


def lcm(*nums):
    return reduce(lambda a, b: a // gcd(a, b) * b, nums)


@lru_cache(maxsize=None)
def h(meter_tuple):
    n = len(meter_tuple)
    if 0 in meter_tuple:
        winning_meter = meter_tuple.index(0)
        res = [1 if meter == winning_meter else 0 for meter in range(n)]
    else:
        probabilities = meter_tuple
        moves = (tuple((meter - 1 if i == idx else meter) for idx, meter in enumerate(meter_tuple))
                 for i in range(n))
        res = [0] * n
        for p, m in zip(probabilities, moves):
            l = h(m)
            for i, v in enumerate(l):
                res[i] += p * v
    return res


def pick_until_match(meters, points):
    key_map = {i: k for i, k in enumerate(meters.keys())}
    meter_tuple = tuple(meters[key_map[i]] for i in range(len(meters)))
    res = defaultdict(int)
    solution = h(meter_tuple)
    for i, p in enumerate(solution):
        res[points[key_map[i]]] += p
    least_common_denominator = lcm(*(f.denominator for f in res.values()))
    res = {k: f.numerator * (least_common_denominator // f.denominator)
           for k, f in res.items()}
    d = reduce(gcd, res.values())
    return {k: v // d for k, v in res.items()}


def investigate_solution(meters):
    print('meters', meters)
    solution = h(meters)
    denominator = lcm(*(f.denominator for f in solution))
    print('solution:', [str(f) for f in solution])
    print('denominator:', denominator)
    denominators, solutions = [], []
    for i, v in enumerate(meters):
        t = tuple(v - 1 if i == j else v for j, v in enumerate(meters))
        s = h(t)
        solutions.append(s)
        denominators.append(lcm(*(f.denominator for f in s)))
    m = lcm(*denominators)
    print('m:', m)
    solutions = [[f.numerator * m // f.denominator for f in s] for s in solutions]
    print('solutions:', solutions)
    res = [0] * len(meters)
    for k, s in zip(meters, solutions):
        for i, v in enumerate(s):
            res[i] += k * v
    g = reduce(gcd, res)
    print('g:', g)
    for k, v in enumerate(res):
        res[k] = v // g
    print('res:', res)


if __name__ == '__main__':
    n = 2
    # meters = {'W': n, 'A': 1, 'B': 1, 'C': 1}
    # points = {'W': 1, 'A': 0, 'B': 0, 'C': 0}
    # meters = {'A': 5, 'B': 5, 'C': 5, 'D': 4, 'E': 2, 'F': 2, 'G': 2}
    # points = {'A': 500, 'B': 500, 'C': 20, 'D': 5, 'E': 5, 'F': 5, 'G': 2}
    # meters = {'A': 4, 'B': 2, 'C': 2, 'D': 2, 'E': 2, 'F': 2, 'G': 2}
    # points = {'A': 1000, 'B': 200, 'C': 50, 'D': 5, 'E': 5, 'F': 2, 'G': 1}
    # meters = {'A': 5, 'B': 5, 'C': 4, 'D': 4, 'E': 4, 'F': 3, 'G': 2}
    # points = {'A': 1000, 'B': 1000, 'C': 500, 'D': 100, 'E': 25, 'F': 25, 'G': 20}
    meters = (5, 3, 1)
    investigate_solution(meters)
    print(h)

    # {0: 10, 1: 3, 2: 6, *, 4: 2, 5: 5, 6: 8, 7: 1, 8: 4, 9: 7}
    # [0, 7, 4, 1, 8, 5, 2, 9, 6, 3]

"""
Notes:

meters (5, 3, 2)
solution: ['9/56', '13/40', '18/35']
denominator: 280
d: 2520
solutions: [[520, 768, 1232], [320, 1100, 1100], [245, 525, 1750]]
g: 90
res: [45, 91, 144]

meters (4, 3, 2)
solution: ['13/63', '32/105', '22/45']
denominator: 315
d: 840
solutions: [[231, 231, 378], [140, 350, 350], [108, 165, 567]]
g: 24 = 3 * 8
res: [65, 96, 154] = [520, 768, 1232] (* 8)

meters (5, 2, 2)
solution: ['8/63', '55/126', '55/126']
denominator: 126
d: 168
solutions: [[28, 70, 70], [13, 105, 50], [13, 50, 105]]
g: 12
res: [16, 55, 55] = [320, 1100, 1100] (* 20) = [192, 660, 660] (* 12)

meters (5, 3, 1)
solution: ['7/72', '5/24', '25/36']
denominator: 72
d: 840
solutions: [[108, 165, 567], [65, 250, 525], [0, 0, 840]]
g: 105 = 3 * 35
res: [7, 15, 50] = [245, 525, 1750] (* 35)


"""
