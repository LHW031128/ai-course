import unittest
from calc import calculate

class TestCalculator(unittest.TestCase):

    # 1. Basic Arithmetic
    def test_addition(self):
        self.assertEqual(calculate("1 + 1"), 2)
        self.assertEqual(calculate("10 + 20"), 30)
        self.assertEqual(calculate("0.1 + 0.2"), 0.30000000000000004) # Standard float behavior

    def test_subtraction(self):
        self.assertEqual(calculate("10 - 5"), 5)
        self.assertEqual(calculate("5 - 10"), -5)

    def test_multiplication(self):
        self.assertEqual(calculate("3 * 4"), 12)
        self.assertEqual(calculate("3 * -4"), -12)

    def test_division(self):
        self.assertEqual(calculate("10 / 2"), 5)
        self.assertEqual(calculate("10 / 4"), 2.5)

    # 2. Operator Precedence
    def test_precedence(self):
        self.assertEqual(calculate("2 + 3 * 4"), 14)
        self.assertEqual(calculate("2 * 3 + 4"), 10)
        self.assertEqual(calculate("10 - 4 / 2"), 8)
        self.assertEqual(calculate("10 / 2 - 3"), 2)

    # 3. Parentheses
    def test_parentheses(self):
        self.assertEqual(calculate("(2 + 3) * 4"), 20)
        self.assertEqual(calculate("10 / (2 + 3)"), 2)
        self.assertEqual(calculate("((2 + 3) * 2) / 2"), 5)

    # 4. Negative Numbers and Floats
    def test_negative_and_floats(self):
        self.assertEqual(calculate("-5 + 3"), -2)
        self.assertEqual(calculate("5 + -3"), 2)
        self.assertEqual(calculate("-5 * -5"), 25)
        self.assertEqual(calculate("3.14 * 2"), 6.28)
        self.assertEqual(calculate("-3.14 + 1"), -2.14)
        self.assertEqual(calculate("--5"), 5) # Double negation

    # 5. Exception Handling
    def test_zero_division(self):
        with self.assertRaises(ZeroDivisionError):
            calculate("10 / 0")
        with self.assertRaises(ZeroDivisionError):
            calculate("10 / (5 - 5)")

    def test_invalid_expressions(self):
        with self.assertRaises(ValueError):
            calculate("2 + * 3")
        with self.assertRaises(ValueError):
            calculate("2 + (3")
        with self.assertRaises(ValueError):
            calculate("abc")
        with self.assertRaises(ValueError):
            calculate("")
        with self.assertRaises(ValueError):
            calculate(None)

    # Additional cases to reach 20+
    def test_complex_expressions(self):
        self.assertEqual(calculate("1 + 2 * (3 + 4) / 2"), 8.0)
        self.assertEqual(calculate("100 - (20 * 3 + 10)"), 30)
        self.assertEqual(calculate("0.5 * 0.5"), 0.25)
        self.assertEqual(calculate("10 / 0.5"), 20)
        self.assertEqual(calculate("-1 + -1"), -2)
        self.assertEqual(calculate("1.5 + 2.5"), 4)

if __name__ == '__main__':
    unittest.main()
