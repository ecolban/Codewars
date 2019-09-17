from random import choice
from time import time as now

def jumbled_string(s, n):
    processed, permutation = set(), {}
    len_s = len(s)
    for i in range(len_s):
        if i not in processed:
            processed.add(i)
            j, cycle = i, [i]
            while True:
                if j % 2 == 1: j += len_s
                j //= 2
                if i == j: break
                cycle.append(j)
                processed.add(j)
            for j, k in enumerate(cycle):
                permutation[cycle[(j + n) % len(cycle)]] = k
    return ''.join(s[permutation[i]] for i in range(len_s))


def max_cycle(m):
    processed, lcm = set(), 1
    for i in range(m):
        if i not in processed:
            processed.add(i)
            j, count = i, 1
            while True:
                if j % 2 == 1: j += m
                j //= 2
                if i == j: break
                count += 1
                processed.add(j)
            lcm = lcm * count // gcd(lcm, count)
    return lcm


def gcd(a, b):
    return b if a == 0 else gcd(b % a, a)


# print(max((max_cycle(i), i) for i in range(199000, 200000)))
# a = [i for i in range(9500, 10500) if max_cycle(i) > i - 2]
# print(a)
# print(len(a))
# print(jumbled_string("Such Wow!", 1))

# chars = '''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789~!@#$%^&*()_-+=[{]}\|;:'",.<>/? '''
# string = ''.join(choice(chars) for _ in range(19998))


def generate_random_string(n):
    alphabet = '''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789~!@#$%^&*()_-+=[{]}\|;:'",.<>/? '''
    return ''.join(choice(alphabet) for _ in range(n))


# print(max_cycle(len(string)))
# print(len(chars))

# print(all(string == jumbled_string(string, 19996) for _ in range(10)))


def jumbled_string2(s, n):
    iterations = [s]
    while True:
        s = s[::2] + s[1::2]
        if s == iterations[0]: break
        iterations.append(s)
    return iterations[n % len(iterations)]


# start = now()
# for n in a:
#     s = generate_random_string(n)
#     jumbled_string(s, n - 1)
# print(now() - start)
#
# start = now()
# for n in a:
#     s = generate_random_string(n)
#     jumbled_string2(s, n - 1)
# print(now() - start)


def rev_string(s, n):
    processed, permutation = set(), {}
    len_s = len(s)
    mid = len_s // 2
    for i in range(len_s):
        if i not in processed:
            processed.add(i)
            j, cycle = i, [i]
            while True:
                j = 2 * j + 1 if j < mid else 2 * (len_s - j - 1)
                if i == j: break
                cycle.append(j)
                processed.add(j)
            for j, k in enumerate(cycle):
                permutation[cycle[(j + n) % len(cycle)]] = k
    return ''.join(s[permutation[i]] for i in range(len_s))


print(rev_string('String', 3))