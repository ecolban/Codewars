from collections import defaultdict


def solve(p):
    """See codewars.com kata Divisible by primes."""
    n = p - 1
    for f in factors(n):
        m = n // f
        if pow(10, m, p) == 1:
            n = m
    return '%d-altsum' % (n // 2) if n % 2 == 0 else '%d-sum' % n


def factors(n):
    m = 2
    while m * m <= n:
        if n % m == 0:
            yield m
            n //= m
        else:
            m += 1 if m == 2 else 2
    if n > 1:
        yield n


# Sieve of Eratosthenes
# Code by David Eppstein, UC Irvine, 28 Feb 2002
# http://code.activestate.com/recipes/117119/

def gen_primes():
    """ Generate an infinite sequence of prime numbers.
    """
    # Maps composites to primes witnessing their compositeness.
    # This is memory efficient, as the sieve is not "run forward"
    # indefinitely, but only as long as required by the current
    # number being tested.
    #
    sieve = defaultdict(list)

    # The running integer that's checked for primeness
    q = 2

    while True:
        if q not in sieve:
            # q is a new prime.
            # Yield it and mark its first multiple that isn't
            # already marked in previous iterations
            #
            yield q
            sieve[q * q] = [q]
        else:
            # q is composite. sieve[q] is the list of primes that
            # divide it. Since we've reached q, we no longer
            # need it in the map, but we'll mark the next
            # multiples of its witnesses to prepare for larger
            # numbers
            #
            for p in sieve[q]:
                sieve[p + q].append(p)
            del sieve[q]

        q += 1


if __name__ == '__main__':
    g = gen_primes()
    prev = next(g)
    while prev < 9000:
        current = next(g)
        if current - prev == 2:
            print(prev, current)
        prev = current
