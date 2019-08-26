import kotlin.test.assertEquals
import org.junit.Test
import kotlin.random.Random

class TestExample {
    @Test
    fun example() {
        assertEquals("1-sum", solve(3))
        assertEquals("3-altsum", solve(7))
        assertEquals("1-altsum", solve(11))
        assertEquals("3-altsum", solve(13))
        assertEquals("3-sum", solve(37))
        assertEquals("23-altsum", solve(47))
        assertEquals("4-altsum", solve(73))
        assertEquals("7-sum", solve(239))
        assertEquals("47006-altsum", solve(376049))
        assertEquals("499941-sum", solve(999883))
        assertEquals("12350861-sum", solve(24701723))
        assertEquals("11484850-altsum", solve(45939401))
    }

    @Test
    fun random() {
        val primeList = primes(50_000_000)
        repeat(100) {
            val i: Int = Random.nextInt(0, primeList.size)
            val p = primeList[i].toLong()
            assertEquals(expectedSolution(p), solve(p))
        }
    }

    private fun expectedSolution(p: Long): String {
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

    private fun primes(n: Int): List<Int> {
        val sieve = BooleanArray((n - 1) / 2) { true }
        val hi = (Math.sqrt(n.toDouble()).toInt() - 2) / 2
        for (j in 0..hi) {
            if (sieve[j]) {
                val i = 2 * j + 3
                for (k in (i * i - 3) / 2..(n - 3) / 2 step i) {
                    sieve[k] = false
                }
            }
        }
        return listOf(2) + (3..n step 2).filter { sieve[(it - 3) / 2] }
    }
}