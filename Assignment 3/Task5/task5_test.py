"""
Although this file is named test_task4.py it is where you will work
for task 5.
The provided testcase is quite verbose and not all tests should be as
detailed in their documentation.

Please also note that the provided example only provides one "test"
this would be marked as unsatisfactory. Please include multiple different cases for each test.
"""
import unittest
from task4 import BankAccount  # assume this is the provided class
from custom_errors import *


class TestBankAccount(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        BankAccount.set_next_account_number(1045)
        BankAccount.unban_all()

    def setUp(self) -> None:
        BankAccount.set_next_account_number(1045)
        BankAccount.unban_all()

    def test_valid_deposit(self):
        """
        1.1 Valid deposit.
        Test the deposit method of the BankAccount class to ensure it correctly adds
        the deposited amount to the account balance.

        Steps:
        1. Create a BankAccount instance with an initial balance of 1000 (+ 49.99 the bonus amount).
        2. Deposit 500 into the account.
        3. Assert that the account balance is updated to 1549.99 (Inital 1000 + 49.99 (from the bonus) + 500 (from the deposit)).

        Assertion:
        - Verify that the account balance after the deposit is 1549.99, indicating
          that the deposit method works as expected.
        """
        account = BankAccount("John Doe", 1000)
        account.deposit(500)
        self.assertEqual(account.balance, 1549.99,
                         f"Deposit method failed to update balance correctly. Expected 1549.99, got {account.balance}")

    def test_invalid_balance_type(self):
        """1.2 Check bank init balance type assertion"""
        # Example of how to check if an error is being raised
        with self.assertRaises(CustomTypeError,
                               msg="Expected a type error to be raised when making a bank account with the balance "
                                   "'fifty'. Either no error or the incorrect error was raised."):
            BankAccount("Rupert", "fifty")

    def test_valid_constructor(self):
        first_account = BankAccount("John", 1000)
        second_account = BankAccount("Jimmy", 500)

        self.assertEqual(first_account.owner, "John",
                         msg=f"Owner name was set to {first_account.owner}, expected 'John'")
        self.assertEqual(first_account.balance, 1049.99, msg=f"Account Balance = {first_account.balance}, expected "
                                                             f"balance = 1049.99 (including bonus")
        self.assertEqual(first_account.account_number, 1045,
                         msg=f"Account number was  {first_account.account_number}, expected 1046")

        self.assertEqual(second_account.owner, "Jimmy",
                         msg=f"Owner name was set to {first_account.owner}, expected 'Jimmy'")
        self.assertEqual(second_account.balance, 549.99, msg=f"Account number was  {first_account.account_number},"
                                                             f"expected 549.99")
        self.assertEqual(second_account.account_number, 1046,
                         msg=f"Account number was  {first_account.account_number}, "
                             f"expected 1047")

    def test_owner_type(self):
        with self.assertRaises(CustomTypeError, msg=f"Expected a value for owner of type string"):
            BankAccount(123, 1000)

    def test_empty_owner(self):
        with self.assertRaises(CustomValueError, msg=f"Expected a non empty string value for owner"):
            BankAccount('', 1000)

    def test_balance_type(self):
        with self.assertRaises(CustomTypeError, msg=f"Expected a numeric value for balance"):
            BankAccount("Oliver", 'One Hundred')

    def test_negative_balance(self):
        with self.assertRaises(CustomValueError, msg=f"Expected a positive numeric value for balance. Got a negative "
                                                     f"value instead."):
            BankAccount("Oliver", -125)

    def test_next_account(self):
        BankAccount.set_next_account_number(2025)
        account = BankAccount("Ema", 2020)

        self.assertEqual(account.account_number, 2025, msg=f"Account number was set to {account.account_number}, "
                                                           f"expected 2025")

    def test_banning_accounts(self):
        account = BankAccount("Ema", 1000)
        self.assertFalse(account.is_banned(), msg=f"New account created should not be banned initially")

        account.ban_account('financial fraud')
        self.assertTrue(account.is_banned(), msg=f"Account should be banned after calling ban_account() method")
        self.assertEqual(account.ban_reason, "financial fraud", msg=f"Ban reason was {account.ban_reason}, expected "
                                                                    f"'financial fraud'")

    def test_invalid_ban_reason(self):
        account = BankAccount("Grace", 300)
        with self.assertRaises(CustomTypeError, msg=f"Ban reason must be of type string"):
            account.ban_account(123456)

    def test_deposit(self):
        account = BankAccount("William", 2000)
        initial_balance = account.balance
        account.deposit(100)
        self.assertEqual(account.balance, initial_balance + 100,
                         msg=f"Balance after deposit is {account.banned_accounts}, expected {initial_balance + 50}")

    def test_banned_deposit(self):
        account = BankAccount("Jonathan", 1500)
        account.ban_account("Financial Fraud")
        with self.assertRaises(CustomOperationError, msg=f"Depositing into a banned account is not possible"):
            account.deposit(100)

    def test_deposit_type(self):
        account = BankAccount("Ivan", 1000)
        with self.assertRaises(CustomTypeError, msg=f"Deposit amount should be numeric"):
            account.deposit("fifty")

    def test_zero_deposit(self):
        account = BankAccount("Ivan", 1000)
        with self.assertRaises(CustomValueError, msg=f"Deposit amount must be non zero"):
            account.deposit(0)

    def test_negative_deposit(self):
        account = BankAccount("Ivanka", 2000)
        with self.assertRaises(CustomValueError, msg=f"Deposit amount must be non negative"):
            account.deposit(-100)

    def test_withdraw_from_banned_account(self):
        account = BankAccount("Steve", 2000)
        account.ban_account("Fraud")

        with self.assertRaises(CustomOperationError, msg=f"Cannot withdraw funds from a banned account"):
            account.withdraw(100)

    def test_withdraw_amount_type(self):
        account = BankAccount("Prajwal", 1000)
        withdraw_amount = 'Withdraw'

        with self.assertRaises(CustomTypeError, msg=f"Withdraw amount has to be of type numeric"):
            account.withdraw(withdraw_amount)

    def test_zero_withdrawal(self):
        account = BankAccount("Shahid", 1000)
        withdraw_amount = 0

        with self.assertRaises(CustomValueError, msg=f"Withdrawal amount must be greater than 0"):
            account.withdraw(withdraw_amount)

    def test_negative_withdrawal(self):
        account = BankAccount("Harper", 1000)
        withdrawal_amount = -100

        with self.assertRaises(CustomValueError, msg=f"Withdrawal amount must be a non zero positive number"):
            account.withdraw(withdrawal_amount)

    def test_withdrawal_limit(self):
        account = BankAccount("Grey", 1000)
        withdrawal_amount = account.balance + 100

        with self.assertRaises(CustomLimitError, msg=f"Cannot withdraw an amount greater than the account's balance"):
            account.withdraw(withdrawal_amount)

    def test_withdrawal_limit_transaction_limit(self):
        account = BankAccount("Berlin", 1000)
        account.set_transaction_limit(100)

        with self.assertRaises(CustomLimitError, msg=f"Cannot withdraw amount greater than transaction limit"):
            account.withdraw(200)

    def test_valid_transfer(self):
        first_account = BankAccount("Tokyo", 1000)
        second_account = BankAccount("Nairobi", 2000)

        first_account_initial_balance, second_account_initial_balance = first_account.balance, second_account.balance

        transfer_amount = 500
        first_account.transfer_to(second_account, transfer_amount)

        self.assertEqual(
            first_account.balance,
            first_account_initial_balance - transfer_amount,
            msg=f"Source account balance after transfer is {first_account.balance}, "
                f"expected {first_account_initial_balance - transfer_amount}"
        )

        self.assertEqual(
            second_account.balance,
            second_account_initial_balance + transfer_amount,
            msg=f"Target account balance after transfer is {second_account.balance}, "
                f"expected {second_account_initial_balance + transfer_amount} "
        )

    def test_invalid_transfer_type(self):
        first_account = BankAccount("Helsinki", 4000)

        with self.assertRaises(CustomTypeError, msg=f"Transferring funds to a non BankAccount is not possible"):
            first_account.transfer_to("Denver", 100)

    def test_invalid_transfer_amount_type(self):
        first_account = BankAccount("Professor", 6000)
        second_account = BankAccount("Lisbon", 1000)

        with self.assertRaises(CustomTypeError, msg=f"Transfer amount should be of type numeric"):
            first_account.transfer_to(second_account, "1244")

    def test_zero_transfer_amount(self):
        first_account = BankAccount("Ohio", 1000)
        second_account = BankAccount("Rome", 1000)

        with self.assertRaises(CustomValueError, msg=f"Transfer amount should be non zero and numeric"):
            first_account.transfer_to(second_account, 0)

    def test_negative_transfer_amount(self):
        first_account = BankAccount("Ohio", 1000)
        second_account = BankAccount("Rome", 1000)

        with self.assertRaises(CustomValueError, msg=f"Transfer amount has to be a non negative number"):
            first_account.transfer_to(second_account, -100)

    def test_transfer_when_insufficient_balance(self):
        first_account = BankAccount("Ohio", 1000)
        second_account = BankAccount("Rome", 1000)

        with self.assertRaises(CustomLimitError, msg=f"Cannot transfer an amount greater than available balance"):
            first_account.transfer_to(second_account, first_account.balance + 1)

    def test_transfer_above_transaction_limit(self):
        first_account = BankAccount("Ohio", 1000)
        second_account = BankAccount("Rome", 1000)

        transaction_limit = 100
        first_account.set_transaction_limit(transaction_limit)

        with self.assertRaises(CustomLimitError,
                               msg=f"Cannot transfer funds greater than transaction limit set for source account"):
            first_account.transfer_to(second_account, transaction_limit + 1)

    def test_transfer_to_banned_account(self):
        first_account = BankAccount("Ohio", 1000)
        second_account = BankAccount("Rome", 1000)

        first_account.ban_account("Criminal")

        with self.assertRaises(CustomOperationError, msg=f"Cannot transfer money from a banned bank account"):
            first_account.transfer_to(second_account, 100)

        with self.assertRaises(CustomOperationError, msg=f"Cannot transfer money to a banned account"):
            second_account.transfer_to(first_account, 100)

    def test_set_valid_transaction_limit(self):
        first_account = BankAccount("Ohio", 1000)
        transaction_limit = 100
        first_account.set_transaction_limit(transaction_limit)

        self.assertEqual(first_account.transaction_limit, transaction_limit, msg=f"Transaction limit was set to "
                                                                                 f"{first_account.transaction_limit}, "
                                                                                 f"expected {transaction_limit}")

        first_account.transaction_limit = None

        self.assertEqual(first_account.transaction_limit, None, msg=f"Transaction limit was set to "
                                                                    f"{first_account.transaction_limit}"
                                                                    f"expected {None}")

    def test_set_invalid_transaction_limit(self):
        first_account = BankAccount("Ohio", 1000)
        transaction_limit = 'limit'

        with self.assertRaises(CustomTypeError, msg=f"Transaction limit should be of type numeric"):
            first_account.set_transaction_limit(transaction_limit)

    def test_set_zero_transaction_limit(self):
        first_account = BankAccount("Ohio", 1000)
        transaction_limit = 0

        with self.assertRaises(CustomValueError, msg=f"Transaction limit should be a non zero number"):
            first_account.set_transaction_limit(transaction_limit)

    def test_set_negative_transaction_limit(self):
        first_account = BankAccount("Ohio", 1000)
        transfer_amount = -100

        with self.assertRaises(CustomValueError, msg=f"Transfer limit should be a non negative number"):
            first_account.set_transaction_limit(transfer_amount)

    def test_str_method_for_no_limit_no_ban(self):
        first_account = BankAccount("Ohio", 1000)
        account_holder_name = first_account.owner
        str_representation = str(first_account)

        self.assertIn(f"{account_holder_name}'s account", str_representation, msg=f"String representation of "
                                                                                  f"BankAccount object should contain "
                                                                                  f"the owner's name")

        self.assertIn(f"{first_account.account_number}", str_representation, msg=f"String representation of "
                                                                                 f"BankAccount object should contain "
                                                                                 f"the owner's account number")

        self.assertIn(f"Balance=$", str_representation, msg=f"String representation of "
                                                            f"BankAccount object should contain "
                                                            f"the owner's account balance")
        self.assertIn(f"Limit=$N/A", str_representation, msg=f"String representation of BankAccount object should show "
                                                             f"'Limit=$N/A' when no limit is set")

        self.assertIn(f"Banned=No", str_representation, msg=f"String representation of "
                                                            f"BankAccount object should show "
                                                            f"Banned=No when account is not banned")

    def test_str_method_with_limit_and_ban(self):
        first_account = BankAccount("Ohio", 1000)
        first_account.set_transaction_limit(100)
        ban_reason = 'Criminal'
        first_account.ban_account(ban_reason)

        str_representation = str(first_account)

        self.assertIn('Limit=$100.00', str_representation, msg=f"String representation should show limit when the "
                                                               f"limit is set")

        self.assertIn("Banned=Yes", str_representation, msg=f"String representation should show 'Banned=Yes' when "
                                                            f"account is banned")

        self.assertIn(f"Ban Reason: {ban_reason}", str_representation, msg=f"String representation should include ban "
                                                                           f"reason when the account is banned")

    @classmethod
    def tearDownClass(cls) -> None:
        BankAccount.unban_all()


if __name__ == "__main__":
    unittest.main()
