import unittest
from src.calculator import sum


class CalculatorTests(unittest.TestCase):
    def test_sum(self):
        assert sum(2, 3) == 5

    def test_sum_negative(self):
        assert sum(-2, 3) == 1

    def test_sum_negative_both(self):
        assert sum(-2, -3) == -5
