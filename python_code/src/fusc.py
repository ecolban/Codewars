from time import perf_counter


def _fusc(n):
    A, B = 0, 1
    # i=0
    while True:
        # i+=1
        # print(f" A {A}  B {B}  n {n} ")
        if n == 0:
            return A
        if n % 2 == 0:
            B += A
            n = n >> 1
        else:
            A += B
            n = (n - 1) >> 1


def _fusc2(n):
    A, B = 0, 1
    while n > 0:
        if n & 1:
            A += B
        else:
            B += A
        n = n >> 1
    return A


def fusc(n):
    a, b = 0, 1
    for i in reversed(bin(n)[2:]):
        if i == '1':
            a += b
        else:
            b += a
    return a


if __name__ == "__main__":
    start = perf_counter()
    print(fusc(98709587209587))
    print((perf_counter() - start) * 1000)
