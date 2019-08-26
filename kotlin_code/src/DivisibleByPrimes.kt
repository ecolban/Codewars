fun solve(p: Long): String {
    var n = p - 1
    for (f in factors(p - 1)) {
        val m = n / f
        if (10L.pow(m, p) == 1L) n = m
    }
    return if (n % 2L == 1L) "$n-sum" else "${n / 2}-altsum"
}

private fun factors(n: Long): Sequence<Long> = sequence {
    var m = n
    var d = 2L
    while (d * d <= n) {
        while (m % d == 0L) {
            yield(d)
            m /= d
        }
        d += if (d == 2L) 1L else 2L
    }
    if (m > 1) yield(m)
}

private fun Long.pow(exp: Long, mod: Long): Long {
    var a = exp
    var b = 1L
    var res = 1L
    while (b <= exp) b = b shl 1
    while (b > 1L) {
        b = b shr 1
        res = res * res % mod
        if (b <= a) {
            a -= b
            res = res * this % mod
        }
    }
    return res
}
