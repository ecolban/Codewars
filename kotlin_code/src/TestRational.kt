import kotlin.test.*
import org.junit.Test


class RationalTest {
    @Test
    fun testAddition() {
        expect(Rational(3, 4)) {
            Rational(1, 2) + Rational(1, 4)
        }
    }

    @Test
    fun testSubstraction() {
        expect(Rational(1, 6)) {
            Rational(1, 2) - Rational(1, 3)
        }
    }

    @Test
    fun testMultiplication() {
        expect(Rational(5, 4)) {
            Rational(1, 2) * Rational(5, 2)
        }
    }

    @Test
    fun testDivision() {
        expect(Rational(5, 4)) {
            Rational(1, 2) / Rational(2, 5)
        }
    }


    @Test
    fun testParseString() {
        expect(Rational(1, 2)) { Rational.parse("0.5") }
        expect(Rational(3, 5)) { Rational.parse("0.6") }

    }

    @Test
    fun testToString() {
        expect("-12/13"){ Rational(24, -26).toString()}
        expect("NaN"){Rational(0, 0).toString()}
        expect("-Infinity"){Rational(-1, 0).toString()}
    }

    @Test
    fun simplifyTest() {
        expect(Rational(1, 2)) { Rational(2, 4) }
    }


    @Test
    fun greaterThanTest() {
        assertTrue(Rational(6, 13) < Rational(10, 21))
        assertTrue(Rational.POSITIVE_INFINITY < Rational.NaN)
        assertTrue(Rational.NEGATIVE_INFINITY < Rational(-1, 2))
        assertTrue(Rational(-1, 2) < Rational.POSITIVE_INFINITY)
        assertTrue(Rational.NEGATIVE_INFINITY < Rational.POSITIVE_INFINITY)
    }
}