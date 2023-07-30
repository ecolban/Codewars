from time import time


def floyd(f, x_0):
    """Floyd's cycle detection algorithm."""
    # Main phase of algorithm: finding a repetition x_i = x_2i.
    # The hare moves twice as quickly as the tortoise and
    # the distance between them increases by 1 at each step.
    # Eventually they will both be inside the cycle and then,
    # meet at some point x_i. The tortoise has moved i steps,
    # whereas the hare has moved 2 * i steps. The difference of
    # i steps must correspond to n * λ, for some n.
    tortoise, hare = f(x_0), f(f(x_0))
    while tortoise != hare:
        tortoise, hare = f(tortoise), f(f(hare))
    # The tortoise goes back to start and the hare stays at x_i.
    # The tortoise and the hare move at the same pace. After i steps,
    # the hare will have gone n times (since i == n * λ) around the
    # loop and be at x_i and the tortoise will also be at x_i. But to
    # reach x_i at the same time, they must reach the entrance of the
    # loop x_μ at the same time.
    tortoise, mu = x_0, 0
    while tortoise != hare:
        tortoise, hare = f(tortoise), f(hare)
        mu += 1
    tortoise, lam = f(tortoise), 1
    while tortoise != hare:
        tortoise = f(tortoise)
        lam += 1
    return mu, lam


def brent(f, x0) -> tuple[int, int]:
    """Brent's cycle detection algorithm."""
    # main phase: search successive powers of two
    power = lam = 1
    tortoise = x0
    hare = f(x0)  # f(x0) is the element/node next to x0.
    while tortoise != hare:
        if power == lam:  # time to start a new power of two?
            tortoise = hare
            power *= 2
            lam = 0
        hare = f(hare)
        lam += 1

    # Find the position of the first repetition of length lam
    tortoise = hare = x0
    for i in range(lam):
        # range(lam) produces a list with the values 0, 1, ... , lam-1
        hare = f(hare)
    # The distance between the hare and tortoise is now lam.

    # Next, the hare and tortoise move at same speed until they agree
    mu = 0
    while tortoise != hare:
        tortoise = f(tortoise)
        hare = f(hare)
        mu += 1

    return mu, lam


def h(m):
    def f(p):
        a, b = p
        return b, (a + b) % m

    return f


if __name__ == "__main__":
    start = (0, 1)
    start_time = time()
    print(floyd(h(100_000_000), start))
    print(f'Time: {int((time() - start_time) * 1000)}ms')
    # (0, 150000000)
    # Time: 43352ms

    start_time = time()
    print(brent(h(100_000_000), start))
    print(f'Time: {int((time() - start_time) * 1000)}ms')
    # (0, 150000000)
    # Time: 50151ms
