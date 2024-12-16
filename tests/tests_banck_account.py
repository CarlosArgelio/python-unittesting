import os
import unittest

from src.banck_account import BankAccount


class BankAccountTests(unittest.TestCase):

    def setUp(self):
        self.account = BankAccount(balance=1000, log_file="transation_log.txt")

    def tearDown(self):
        if os.path.exists(self.account.log_file):
            os.remove(self.account.log_file)

    def _count_lines(self, filename):
        with open(filename) as f:
            return len(f.readlines())

    def test_deposit(self):
        self.account.deposit(100)
        self.assertEqual(self.account.balance, 1100)

    def test_withdraw(self):
        self.account.withdraw(100)
        self.assertEqual(self.account.balance, 900)

    def test_get_balance(self):
        self.assertEqual(self.account.get_balance(), 1000)

    def test_transaction_log(self):
        self.account.deposit(100)
        assert os.path.exists("transation_log.txt")

    def test_count_transation(self):
        assert self._count_lines(self.account.log_file) == 1
        self.account.deposit(100)
        assert self._count_lines(self.account.log_file) == 2
