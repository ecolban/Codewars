from heapq import heapify, heappop, heappush
from random import seed, sample
from time import perf_counter
from timeit import timeit


def closure_gen(initial_set: set[int]):
    if 1 in initial_set:
        yield 1
        initial_set.remove(1)
    if not initial_set:
        return
    # numbers generated so far. If 1 was not generated, we pretend it was.
    generated = [1]

    # Every number generated is the product of a number previously generated
    # and a number in initial_set. For e in initial_set, pointers[e] is the
    # least index into generated such that generated[pointers[e]] * e has not
    # yet been generated.
    pointers = {e: 0 for e in initial_set}
    # candidates = [(generated[pointers[e]] * e, e) for e in s]
    candidates = [(e, e) for e in initial_set]

    while True:
        next_value, e = min(candidates)
        yield next_value
        generated.append(next_value)
        for i, (v, e) in enumerate(candidates):
            if v <= next_value:
                pointers[e] += 1
                candidates[i] = (generated[pointers[e]] * e, e)


def get_duplicates(initial_set: set[int]):
    if 1 in initial_set:
        yield 1
        initial_set.remove(1)
    if not initial_set:
        return
    generated = [1]
    pointers = {e: 0 for e in initial_set}
    candidates = [(e, e) for e in initial_set]
    num_duplicates = 0
    while True:
        next_value, e = min(candidates)
        generated.append(next_value)
        if len(generated) == 1000:
            pass
        for i, (v, e) in enumerate(candidates):
            if v <= next_value:
                num_duplicates += 1
                pointers[e] += 1
                candidates[i] = (generated[pointers[e]] * e, e)
        num_duplicates -= 1
        yield num_duplicates


def closure_gen2(s: set[int], max_n):
    if 1 in s:
        yield 1
        s.remove(1)
    if not s:
        return
    h = list(s)
    heapify(h)
    visited = s.copy()
    num_gen = 0
    num_duplicates = 0
    while True:
        n = heappop(h)
        num_gen += 1
        assert num_gen * len(s) == len(h) + num_duplicates + num_gen
        if num_gen % 100 == 0:
            total = len(h) + num_duplicates + num_gen
            f = num_duplicates / num_gen ** 2
            print(f"{num_gen = :,}, {len(h) = :,}, {num_duplicates = :,}, {total = :,}, { f = : .3f}")
        yield n
        for elem in s:
            elem_ = elem * n
            if elem_ not in visited:
                heappush(h, elem_)
                visited.add(elem_)
            else:
                num_duplicates += 1


def get_duplicates2(s: set[int]):
    if 1 in s:
        s.remove(1)
    if not s:
        return
    h = list(s)
    heapify(h)
    visited = s.copy()
    num_gen = 0
    num_duplicates = 0
    while True:
        n = heappop(h)
        num_gen += 1
        for elem in s:
            elem_ = elem * n
            if elem_ not in visited:
                heappush(h, elem_)
                visited.add(elem_)
            else:
                num_duplicates += 1
        yield num_duplicates
        assert (num_gen + 1) * len(s) == len(h) + num_duplicates + num_gen


if __name__ == '__main__':
    total_to_generate = 200_000
    freq = 1000
    ms = (2,10, 100, 1000)  #, 10_000)
    # gen = [get_duplicates({2, 3}) for m in ms]
    gen = [get_duplicates(set(sample(list(range(2, 10_000_000)), m))) for m in ms]
    for i in range(1, total_to_generate + 1):
        ns = [next(g) for g in gen]
        if i % freq == 0:
            print(f"{i:7d}:", *(f"{n / (m * i):.5f}" for m, n in zip(ms, ns)))
