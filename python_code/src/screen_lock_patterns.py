from itertools import combinations, permutations, chain

KEYS = tuple('ABCDEFGHI')
CRITICAL_MOVES = {
    ('A', 'C'): 'B',
    ('A', 'G'): 'D',
    ('A', 'I'): 'E',
    ('B', 'H'): 'E',
    ('C', 'A'): 'B',
    ('C', 'G'): 'E',
    ('C', 'I'): 'F',
    ('D', 'F'): 'E',
    ('F', 'D'): 'E',
    ('G', 'A'): 'D',
    ('G', 'C'): 'E',
    ('G', 'I'): 'H',
    ('H', 'B'): 'E',
    ('I', 'A'): 'E',
    ('I', 'C'): 'F',
    ('I', 'G'): 'H',
}
CRITICAL_KEYS = set(CRITICAL_MOVES.values())


def count_patterns_from(first_point, n):
    if n == 0: return 0
    return sum(is_valid(first_point, permutation)
               for combination in combinations((k for k in KEYS if k != first_point), n - 1)
               for permutation in permutations(combination))


def is_valid(start_key, key_sequence):
    path = [start_key]
    for k1, k2 in zip(chain((start_key,), key_sequence), key_sequence):
        path.append(k2)
        if (k1, k2) in CRITICAL_MOVES and CRITICAL_MOVES[(k1, k2)] not in path:
            return False
    return True


def total(i):
    return 4 * count_patterns_from('A', i) + 4 * count_patterns_from('B', i) + count_patterns_from('E', i)


if __name__ == '__main__':
    print(*(total(i) for i in range(4, 10)))
    print(sum(total(i) for i in range(4, 10)))
