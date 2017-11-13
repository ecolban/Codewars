def nth_survivor(n):
    m = n * n
    for i in range(n - 1, 0, -1):
        m -= (m - 1) % i + 1
    return m


def survivor1(n):
    def survivor_rec(n, k):
        """Returns true if the last element of a sequence of length n survives
        when one starts by killing every k'th element, then every (k+1)th elements,
        then every (k+2)th element, etc."""

        if n < k: return True  # The obvious case first
        q, r = divmod(n, k)
        # If r == 0, then k divides n and the last element dies
        if r == 0: return False
        # Otherwise, we kill q elements, and the sequence is shortened to n - q
        return survivor_rec(n - q, k + 1)

    # Start with a sequence of length n, where n is the last element,
    # and start by killing every second element
    return survivor_rec(n, 2)


def survivor(n):
    k, r = 2, 1
    while k <= n:
        q, r = divmod(n, k)
        if r == 0:
            return False
        n, k = n - q, k + 1
    else:
        return True
