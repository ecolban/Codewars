/*

from functools import lru_cache

def lcs(x, y):
    @lru_cache(maxsize=None)
    def lcs_(i, j):
        if i < 0 or j < 0: return ''
        if x[i] == y[j]: return lcs_(i - 1, j - 1) + x[i]
        return max(lcs_(i - 1, j), lcs_(i, j - 1), key=len)
    return lcs_(len(x) - 1, len(y) - 1)
*/

fun lcs(a: String, b: String): String {
    val memo =  mutableMapOf<Pair<Int, Int>, String>()

    fun helper(i: Int, j: Int): String {
        if (i < 0 || j < 0) return ""
        return memo.getOrPut(i to j, {
            if (a[i] == b[j]) {
                helper(i - 1, j - 1) + a[i]
            } else {
                val alt1 = helper(i - 1, j)
                val alt2 = helper(i, j - 1)
                if (alt1.length >= alt2.length) alt1 else alt2
            }
        })
    }
    return helper(a.length - 1, b.length - 1)
}
