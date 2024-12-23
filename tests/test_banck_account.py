import os
import unittest
from unittest.mock import patch

from src.banck_account import BankAccount
from src.exceptions import WithdrawalTimeRestrictionError

SERVER = "server_a"


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

    # def test_withdraw(self):
    #     self.account.withdraw(100)
    #     self.assertEqual(self.account.balance, 900)

    def test_get_balance(self):
        self.assertEqual(self.account.get_balance(), 1000)

    def test_transaction_log(self):
        self.account.deposit(100)
        assert os.path.exists("transation_log.txt")

    def test_count_transation(self):
        assert self._count_lines(self.account.log_file) == 1
        self.account.deposit(100)
        assert self._count_lines(self.account.log_file) == 2

    @unittest.skip("This test is skipped")
    def test_skip(self):
        self.assertEqual("hola", "chao")

    # @unittest.skipIf(SERVER == "server_a", "Saltada por que no estamos en el servidor")
    # def test_skip_if(self):
    #     if self.account.balance < 1000:
    #         self.skipTest("Balance is less than 1000")
    #     self.account.withdraw(100)
    #     self.assertEqual(self.account.balance, 900)

    @unittest.expectedFailure
    def expected_failure(self):
        self.assertEqual("hola", "chao")

    @patch("src.bank_account.datetime")
    def test_withdraw_during_bussines_hours(self, mock_datetime):
        mock_datetime.now.return_value.hour = 8
        new_balance = self.account.withdraw(100)
        self.assertEqual(new_balance, 900)

    @patch("src.bank_account.datetime")
    def test_withdraw_disallow_before_bussines_hours(self, mock_datetime):
        mock_datetime.now.return_value.hour = 7
        with self.assertRaises(WithdrawalTimeRestrictionError):
            self.account.withdraw(100)

    @patch("src.bank_account.datetime")
    def test_withdraw_disallow_after_bussines_hours(self, mock_datetime):
        mock_datetime.now.return_value.hour = 18
        with self.assertRaises(WithdrawalTimeRestrictionError):
            self.account.withdraw(100)

    def test_deposit_varios_ammounts(self):
        tests_cases = [
            {"ammount": 100, "expected": 1100},
            {"ammount": 3000, "expected": 4000},
            {"ammount": 4500, "expected": 5500},
        ]

        for case in tests_cases:
            with self.subTest(case=case):
                self.account = BankAccount(balance=1000, log_file="transations.txt")
                new_balance = self.account.deposit(case["ammount"])
                self.assertEqual(new_balance, case["expected"])
