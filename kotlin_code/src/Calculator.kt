import java.math.BigDecimal
import java.math.MathContext
import java.util.*

class Calculator {

    private val operandStack: Stack<BigDecimal> = Stack()
    private val operatorStack: Stack<String> = Stack()

    private val DIGITS = setOf("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
    private val BINARY_OPERATORS = setOf("+", "-", "*", "/")
    private val NAN = "Not a number"
    private val precedence = mapOf("+" to 1, "-" to 1, "*" to 2, "/" to 2)

    private var numberMode = false
    private var currentDisplay = "0"

    private var lastOperand = BigDecimal.ZERO
    private var lastOperator: String? = null


    fun enterKey(key: String): String {
        if (currentDisplay == "0" && key == "0"
                || key == "." && currentDisplay.contains('.')
                || currentDisplay == NAN && key != "C") {
            return currentDisplay
        }

        when (key) {
            in DIGITS -> {
                if (!numberMode) enterNumberMode("")
                currentDisplay += key
            }
            "." -> {
                enterNumberMode("0")
                currentDisplay += key
            }
            "+/-" -> {
                if (numberMode) exitNumberMode()
                val n = operandStack.pop()
                operandStack.push(n.negate())
                currentDisplay = n.negate().toString()
            }
            in BINARY_OPERATORS -> {
                if (numberMode) exitNumberMode()
                if (lastOperator != null && precedence(lastOperator!!) >= precedence(key)) {
                    currentDisplay = reduceStack()
                }
                if (lastOperator != null) operatorStack.push(lastOperator)
                lastOperator = key
            }
            "=" -> {
                if (numberMode) exitNumberMode()
                while (!operatorStack.empty()) {
                    currentDisplay = reduceStack()
                }
            }
            "C" -> {
                reset()
            }
            else -> currentDisplay = "0"
        }
        return currentDisplay
    }

    private fun enterNumberMode(initString: String) {
        numberMode = true
        currentDisplay = initString
    }

    private fun exitNumberMode() {
        lastOperand = BigDecimal(currentDisplay, MathContext.DECIMAL128)
        operandStack.push(lastOperand)
        numberMode = false
    }

    private fun reduceStack(): String {
        return try {
            val y = if (operandStack.empty()) lastOperand else operandStack.pop()
            val x = if (operandStack.empty()) lastOperand else operandStack.pop()
            val z = when (operatorStack.pop()) {
                "+" -> x + y
                "-" -> x - y
                "*" -> x * y
                "/" -> x / y
                else -> BigDecimal.ZERO
            }
            operandStack.push(z)
            z.stripTrailingZeros().toPlainString()
        } catch (e: ArithmeticException) {
            NAN
        }
    }

    private fun reset() {
        operandStack.clear()
        operatorStack.clear()
        numberMode = false
        currentDisplay = "0"
    }


    private fun precedence(op: String): Int {
        return precedence[op] ?: 0
    }
}

fun main() {
    val calculator = Calculator()
    for (key in "2 * + - =".split(Regex("\\s+"))) {
        println("$key: ${calculator.enterKey(key)}")
    }
}