import os
import unittest

from src.banck_account import BankAccount


class BankAccountTests(unittest.TestCase):

    def setUp(self):
        self.account = BankAccount(balance=1000, log_file="transation_log.txt")

    def tearDown(self):
        if os.path.exists(self.account.log_file):
            os.remove(self.account.log_file)

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
