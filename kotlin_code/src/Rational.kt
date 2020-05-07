import java.lang.Double.doubleToLongBits
import java.util.regex.Pattern
import kotlin.math.abs

class Rational(numerator: Long, denominator: Long = 1) : Comparable<Rational> {

    private val mNumerator: Long
    private val mDenominator: Long

    init {
        if (denominator == 0L) {
            mNumerator = if (numerator < 0) -1 else if (numerator > 0) 1 else 0
            mDenominator = 0
        } else {
            val d = if (denominator > 0) gcd(numerator, denominator) else -gcd(numerator, denominator)
            mNumerator = numerator / d
            mDenominator = denominator / d
        }

    }


    operator fun plus(other: Rational) =
            Rational(mNumerator * other.mDenominator + mDenominator * other.mNumerator, mDenominator * other.mDenominator)

    operator fun times(other: Rational) =
            Rational(mNumerator * other.mNumerator, mDenominator * other.mDenominator)

    operator fun div(other: Rational) =
            Rational(mNumerator * other.mDenominator, mDenominator * other.mNumerator)

    operator fun minus(other: Rational) =
            Rational(mNumerator * other.mDenominator - mDenominator * other.mNumerator, mDenominator * other.mDenominator)

    operator fun unaryMinus() = Rational(-mNumerator, mDenominator)

    fun toDouble() =
            if (mDenominator == 0L) {
                when {
                    mNumerator < 0L -> Double.NEGATIVE_INFINITY
                    mNumerator > 0L -> Double.POSITIVE_INFINITY
                    else -> Double.NaN
                }
            } else {
                mNumerator.toDouble() / mDenominator.toDouble()
            }


    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        return other is Rational && mNumerator == other.mNumerator && mDenominator == other.mDenominator
    }

    override fun hashCode(): Int = 31 * mNumerator.toInt() + mDenominator.toInt()

    override fun toString(): String {
        return if (mDenominator == 0L) {
            when {
                mNumerator < 0 -> "-Infinity"
                mNumerator > 0 -> "Infinity"
                else -> "NaN"
            }
        } else if (mDenominator == 1L) {
            "$mNumerator"
        } else {
            "$mNumerator/$mDenominator"
        }
    }

    override fun compareTo(other: Rational): Int {
        return when {
            this == NaN -> if (other == NaN) 0 else 1
            other == NaN -> -1
            this == POSITIVE_INFINITY -> if (other == POSITIVE_INFINITY) 0 else 1
            other == POSITIVE_INFINITY -> -1
            this == NEGATIVE_INFINITY -> if (other == NEGATIVE_INFINITY) 0 else -1
            other == NEGATIVE_INFINITY -> 1
            else -> {
                val mNum = mNumerator * other.mDenominator
                val oNum = other.mNumerator * mDenominator
                return mNum.compareTo(oNum)
            }
        }
    }

    companion object {
        val NaN = Rational(0, 0)
        val POSITIVE_INFINITY = Rational(1, 0)
        val NEGATIVE_INFINITY = Rational(-1, 0)

        @Throws(NumberFormatException::class)
        fun parse(s: String): Rational {
            val pattern = Pattern.compile("^[-+]?(\\.\\d+|\\d+\\.?\\d*)$")
            val matcher = pattern.matcher(s)
            if (!matcher.matches()) throw NumberFormatException()
            val idx = s.indexOf('.')
            return if (idx == -1) {
                Rational(s.toLong())
            } else {
                val n = (s.substring(0, idx) + s.substring(idx + 1)).toLong()
                val d = pow10(s.length - idx - 1)
                Rational(n, d)
            }
        }
    }
}

private tailrec fun gcd(a: Long, b: Long): Long = if (a == 0L) abs(b) else gcd(b % a, a)

private tailrec fun gcd_round(a: Long, b: Long): Long =
        if (abs(a.toDouble() / b.toDouble()) < 1e-6) abs(b) else gcd_round(b % a, a)

private fun pow10(n: Int): Long {
    var p = 1L
    var a = n
    var b = 1
    while (b <= n) {
        b = b shl 1
    }
    while (b > 1) {
        b = b shr 1
        p *= p
        if (b <= a) {
            a -= b
            p *= 10
        }
    }
    return p
}

fun Double.toRational(): Rational {
    if (this.isNaN()) return Rational.NaN
    if (this.isInfinite() && this > 0.0) return Rational.POSITIVE_INFINITY
    if (this.isInfinite() && this < 0.0) return Rational.NEGATIVE_INFINITY
    if (this == 0.0) return Rational(0, 1)
    // Stolen from http://goo.gl/4oXPj

    val bits: Long = doubleToLongBits(this)
    val sign: Long = bits ushr 63
    val exponent: Int = (((bits shr 52) and 0x7FFL) - 1023L).toInt()
    val mantissaMask = 0xFFFFFFFFFFFFFL
    val mantissa = bits and mantissaMask
    var b = mantissaMask + 1
    var a = b or mantissa
    if (exponent > 0) {
        if (exponent <= 10) {
            a = a shl exponent
        } else {
            a = a shl 10
            b = b shr (exponent - 10)
        }
    } else if (exponent < 0) {
        if (-exponent <= 10) {
            b = b shl -exponent
        } else {
            a = a shr (-exponent - 10)
            b = b shl 10
        }
    }
    if (sign == 1L) {
        a *= -1L
    }
    val g = gcd(a, b)
    return Rational(a / g, b / g)
}

fun main() {
    println("NaN is greater than positive infinity is ${Double.NaN.compareTo(Double.POSITIVE_INFINITY) > 0}")
    println(Rational.POSITIVE_INFINITY.toDouble())
    val a = Rational.parse("-1.1")
    println("-1.1 = $a")
    val b = Rational.parse("7.8")
    println("7.8 = $b")
    println("When using Rationals: -1.1 + 7.8 = ${(a + b).toDouble()}")
    println("When using Doubles:   -1.1 + 7.8 = ${-1.1 + 7.8}")
    println("10 / 8 = ${Rational(10, 8)}")

    println("(-1.1).toRational() + (7.8).toRational = ${(-1.1).toRational() + (7.8).toRational()}")
    println("(1.01).toRational().toDouble() = ${(1.01).toRational().toDouble()}")
    println("(5.6).toString() = " + (5.6).toString())
    val a1 = 3152519739159347
    val b1 = 562949953421312
    val g = gcd_round(a1, b1)
    println("gcd_round(3152519739159347, 562949953421312) = $g")
    println("3152519739159347 / 562949953421312 = ${Rational(a1 / g, b1 / g)}")
}
