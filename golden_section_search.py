import math

DELTA = 1e-6


def gss_array(a):
    phi = (math.sqrt(5) - 1) / 2
    lo, hi = 0, len(a) - 1
    i, j = int(round((1 - phi) * hi)), int(round(phi * hi))
    lo_val, i_val, j_val, hi_val = a[lo], a[i], a[j], a[hi]
    while hi - lo >= 3:
        if i_val < j_val:
            k = int(round((j - hi) * phi + hi))
            lo, lo_val, i, i_val, j, j_val = i, i_val, j, j_val, k, a[k]
        else:
            k = int(round((i - lo) * phi + lo))
            i, i_val, j, j_val, hi, hi_val = k, a[k], i, i_val, j, j_val
    return max(a[lo:hi + 1])


def gss(fn):
    phi = (math.sqrt(5) - 1) / 2  # golden section
    a, b, c, d, e, f = 0, 1 - phi, phi, 1, None, None
    while d - a >= 2 * DELTA:
        e, f = e or fn(b), f or fn(c)
        a, b, c, d, e, f = (b, c, phi * (d - b) + b, d, f, None) if e < f \
            else (a, phi * (a - c) + c, b, c, None, e)
    return (a + d) / 2
