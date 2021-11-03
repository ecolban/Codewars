from numpy import arange, eye, diag, real
from numpy.linalg import eig, inv

"""
Solution description

The goal is to find the expected score per round when playing the "stop at `n`" strategy.

Assume we are playing the stop_at(6, 20) strategy. Assume furthermore that in a round we have 
reached a score of 19. The next toss of the die may result in a 1, 2, ..., or 6, each with a 
probability of 1/6. The scores are 0, 21, 22, 23,  24, 25 respectively, and so the expected score is 
0/6 + 21/6 + ... + 25/6 = 115/6 = 19 1/6. If, instead, we assume we have reached a score of 18, 
then the expected score after tossing one more time is: 0/6 + 20/6 + ... + 24/6 = 55/3 = 18 1/3.

Now, assume the current score is 17. If we toss a 2, then we reach a score of 19, and in that case the 
expected score is, as we've seen above, 115/6. The expected score given that we've reached 17 is: 
0/6 + (115/6)/6 + 20/6 + ... + 23/6 = 631/36 = 17 19/36.

We can fill a list `a` such that `a[i]` is the expected score given that we have reached a score of `i`. 
We start by initializing `a[n:n + m]` with `[n, n + 1, ..., n + m - 1]`. Then we fill the rest of the 
list by setting `a[i]` to `sum(a[i + 2:i + m + 1]) / m`. When done, `a[0]` gives us the expected score 
at the beginning of the round.

Note that we can write a[i:i + m] in terms of a[i + 1:i + m + 1] by multiplying the latter with a matrix:
`M = [[0, 1/m, 1/m, ..., 1/m, 1/m, 1/m],
      [1,   0,   0, ...,   0,   0,   0],
      [0,   1,   0, ...,   0,   0,   0],
                    ...
      [0,   0,   0, ...,   1,   0,   0],
      [0,   0,   0, ...,   0,   1,   0]]`
     
If `v_0 = a[n:n + m]` and `v_n = a[0:m]`, then `v_n = M^n x v_0` (`M` raised to the power n). 
Using the eigen value decomposition, we can write `M = Q x D x Q^{-1}`, where `Q` is the eigen vector 
matrix and `D` is a diagonal matrix with the corresponsing eigen values on the diagonal.

`M^n = Q x D x inv(Q) x Q x D x inv(Q) x ... x Q x D x inv(Q) = Q x D^n x Q^{-1}`, 
because all the products `Q^{-1} x Q` cancel out. Raising a diagonal matrix to the power n is easy; simply
raise each component to the power n. Hence, using numpy notationn, we get:

`v_n = Q @ D ** n @ inv(Q) @ v_0`.
"""


def stop_at_initial(m, n):
    a = list(range(n + m))
    for i in reversed(range(n)):
        a[i] = sum(a[i + 2:i + m + 1]) / m
    return a[0]


def stop_at(m, n):
    v = range(n, n + m)
    for _ in range(n):
        v = (sum(v[1:]) / m, *v[:-1])
    return v[0]


def stop_at_v(m, n):
    v = arange(n, n + m)
    a = eye(m, k=-1)
    a[0, 1:] = 1 / m
    for _ in range(n):
        v = a @ v
    return v[0]


def stop_at_la(m, n):
    v = arange(n, n + m)
    a = eye(m, k=-1)
    a[0, 1:] = 1 / m
    eigen_values, eigen_vectors = eig(a)
    return real((eigen_vectors @ diag(eigen_values ** n) @ inv(eigen_vectors) @ v)[0])


if __name__ == '__main__':
    print(stop_at_initial(6, 20))
    print(stop_at(6, 20))
    print(stop_at_v(6, 20))
    print(stop_at_la(6, 20))
