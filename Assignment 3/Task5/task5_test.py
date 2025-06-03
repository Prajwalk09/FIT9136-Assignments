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
        """
        This is a class method called before tests in an individual class are run. setUpClass is called with the
        class as the only argument and must be decorated as a class method.

        Parameters:
            This function does not take any inputs.

        Returns:
            This function does not return anything as well.
        """
        BankAccount.set_next_account_number(1045)
        BankAccount.unban_all()

    def setUp(self) -> None:
        """
        This is a Method called to prepare the test fixture. This is called immediately before calling the test
        method; other than AssertionError or SkipTest, any exception raised by this method will be considered an
        error rather than a test failure. The default implementation does nothing.

        Parameters:
            This function does not take any inputs.

        Returns:
            This function does not return anything as well.
        """
        BankAccount.set_next_account_number(1045)
        BankAccount.unban_all()

    def test_valid_deposit(self):
        """
        1.1 Valid deposit.
        Test the deposit method of the BankAccount class to ensure it correctly adds
        the deposited amount to the account balance.

        Steps: 1. Create a BankAccount instance with an initial balance of 1000 (+ 49.99 the bonus amount). 2.
        Deposit 500 into the account. 3. Assert that the account balance is updated to 1549.99 (Initial 1000 + 49.99
        (from the bonus) + 500 (from the deposit)).

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
        """
        Valid Constructor functioning.
        Test the constructor of the BankAccount class and ensure that the objects are being initialised correctly.

        Steps:
        1. Create a BankAccount instance with an initial balance of 1000 (+ 49.99 the bonus amount).
        1. Create another BankAccount instance with an initial balance of 500 (+ 49.99 the bonus amount).
        2. Check all attributes for both the accounts
        3. Assert that the account balance is updated to 1549.99 (Initial 1000 + 49.99 (from the bonus) for the first
           account.

        Assertion:
        - Verify that the account balance after the deposit is 1049.99, indicating
          that the deposit method works as expected and also check whether other attributes are set correctly.
        """
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
        """
        Testing Data Type of Owner
        This function is used to test for the data type of the owner attribute.

        Steps:
            1. Create a bank account with a non string value for the owner.
            2. Assert that the value for the owner attribute has to be of type string

        """
        with self.assertRaises(CustomTypeError, msg=f"Expected a value for owner of type string"):
            BankAccount(123, 1000)

    def test_empty_owner(self):
        """
        Testing Empty Value for Owner
        This function is used to test when the value for the owner is given as an empty_string

        Steps:
            1. Create a bank account with an empty value for the owner
            2. Assert that the value for the owner attribute has to be non-empty and of type string.
        """
        with self.assertRaises(CustomValueError, msg=f"Expected a non empty string value for owner"):
            BankAccount('', 1000)

    def test_balance_type(self):
        """
        Test Balance Type
        This function is used to test the data type of the balance attribute given

        Steps:
            1. Create a bank account with a non-numeric value for balance
            2. Assert that the value for the balance should be of type numeric
        """
        with self.assertRaises(CustomTypeError, msg=f"Expected a numeric value for balance"):
            BankAccount("Oliver", 'One Hundred')

    def test_negative_balance(self):
        """
        Test Negative Balance
        This function is used to test when the balance given is negative

        Steps:
            1. Create a bank account with a negative value for balance.
            2. Assert that the value for the balance should be positive.
        """
        with self.assertRaises(CustomValueError, msg=f"Expected a positive numeric value for balance. Got a negative "
                                                     f"value instead."):
            BankAccount("Oliver", -125)

    def test_zero_balance(self):
        """
        Test Zero Balance
        This function is used to test when the balance given is Zero

        Steps:
            1. Create a bank account with a negative value for balance.
            2. Assert that the value for the balance should be positive and non-zero.
        """
        with self.assertRaises(CustomValueError, msg=f"Expected a positive numeric value for balance. Got 0 instead "
                                                     f"value instead."):
            BankAccount("Oliver", 0)

    def test_next_account(self):
        """
        Test Next Account
        This function is used to test the set_next_account_number

        Steps:
            1. Set the next account number using the next_account_number function.
            2. Create a bank account with an account number, other than the one set earlier.
            3. Assert that the value for the account number should be equal to the one set earlier and not something
               else.
        """
        BankAccount.set_next_account_number(2025)
        account = BankAccount("Ema", 2020)

        self.assertEqual(account.account_number, 2025, msg=f"Account number was set to {account.account_number}, "
                                                           f"expected 2025")

    def test_banning_accounts(self):
        """
        Test Banning Accounts
        This function is used to check if the accounts can be banned correctly.

        Steps:
            1. Create a bank account by giving all the details
            2. Ban that account by giving a reason
            3. Assert that the account should be shown as banned after calling the is_banned method
            4. Assert that the reason given for the ban is correct
        """
        account = BankAccount("Ema", 1000)
        self.assertFalse(account.is_banned(), msg=f"New account created should not be banned initially")

        account.ban_account('financial fraud')
        self.assertTrue(account.is_banned(), msg=f"Account should be banned after calling ban_account() method")
        self.assertEqual(account.ban_reason, "financial fraud", msg=f"Ban reason was {account.ban_reason}, expected "
                                                                    f"'financial fraud'")

    def test_invalid_ban_reason(self):
        """
        Test Invalid Ban Reason
        This function is used to check for invalid type of the ban reason

        Steps:
            1. Create a bank account by giving all the details
            2. Assert that the ban reason has to be of type string.
        """
        account = BankAccount("Grace", 300)
        with self.assertRaises(CustomTypeError, msg=f"Ban reason must be of type string"):
            account.ban_account(123456)

    def test_deposit(self):
        """
        Test Deposit
        This function is used to test for depositing amount into an account.

        Steps:
            1. Create a bank account by giving all the details
            2. Ensure that the balance is properly updated after the deposit.

        """
        account = BankAccount("William", 2000)
        initial_balance = account.balance
        account.deposit(100)
        self.assertEqual(account.balance, initial_balance + 100,
                         msg=f"Balance after deposit is {account.banned_accounts}, expected {initial_balance + 50}")

    def test_banned_deposit(self):
        """
        Test Banned Deposit
        This function is used to ensure that amount cannot be deposited to a banned account

        Steps:
            1. Create a bank account by giving all the details
            2. Ban the account by giving a reason of the correct type.
            3. Assert that depositing money into a banned account is not possible.
        """
        account = BankAccount("Jonathan", 1500)
        account.ban_account("Financial Fraud")
        with self.assertRaises(CustomOperationError, msg=f"Depositing into a banned account is not possible"):
            account.deposit(100)

    def test_deposit_type(self):
        """
        Test Deposit Type
        This function is used to ensure that the deposit amount is of the right type

        Steps:
            1. Create a bank account by giving all the details
            2. Assert that the deposit amount should be numeric
        """
        account = BankAccount("Ivan", 1000)
        with self.assertRaises(CustomTypeError, msg=f"Deposit amount should be numeric"):
            account.deposit("fifty")

    def test_zero_deposit(self):
        """
        Test Zero Deposit
        This function is used to ensure that the deposit amount is non-zero

        Steps:
            1. Create a bank account by giving all the details
            2. Assert that the amount to be deposited has to be non-zero and positive numeric value
        """
        account = BankAccount("Ivan", 1000)
        with self.assertRaises(CustomValueError, msg=f"Deposit amount must be non zero"):
            account.deposit(0)

    def test_negative_deposit(self):
        """
        Test Negative Deposit
        This function is used to ensure that the amount deposited is non-negative

        Steps:
            1. Create a bank account by giving all the details
            2. Assert that the amount to be deposited is non-negative and numeric
        """
        account = BankAccount("Ivanka", 2000)
        with self.assertRaises(CustomValueError, msg=f"Deposit amount must be non negative"):
            account.deposit(-100)

    def test_withdraw_from_banned_account(self):
        """
        Test Withdraw from Banned Account
        This function is used to ensure that amount cannot be withdrawn from an account which is banned.

        Steps:
            1. Create a bank account by giving all the details
            2. Ban the account by giving a reason of valid type
            3. Assert that amount cannot be withdrawn from a banned account
        """
        account = BankAccount("Steve", 2000)
        account.ban_account("Fraud")

        with self.assertRaises(CustomOperationError, msg=f"Cannot withdraw funds from a banned account"):
            account.withdraw(100)

    def test_withdraw_amount_type(self):
        """
        Test Withdraw Amount Type
        This function is used to ensure that the data type of the amount to be withdrawn is numeric

        Steps:
            1. Create a bank account by giving all the details
            2. Use a non-numeric value as an argument to the withdrawal function
            3. Assert that the withdrawal amount should be of type numeric
        """
        account = BankAccount("Prajwal", 1000)
        withdraw_amount = 'Withdraw'

        with self.assertRaises(CustomTypeError, msg=f"Withdraw amount has to be of type numeric"):
            account.withdraw(withdraw_amount)

    def test_zero_withdrawal(self):
        """
        Test Zero Amount
        This function is used to ensure that the withdrawal amount is non-zero

        Steps:
            1. Create a bank account by giving all the details
            2. Use 0 as an argument to the withdrawal function
            3. Assert that the withdrawal amount should be of non-zero
        """
        account = BankAccount("Shahid", 1000)
        withdraw_amount = 0

        with self.assertRaises(CustomValueError, msg=f"Withdrawal amount must be greater than 0"):
            account.withdraw(withdraw_amount)

    def test_negative_withdrawal(self):
        """
        Test Negative Withdrawal Amount
        This function is used to ensure that the withdrawal amount is non-negative

        Steps:
            1. Create a bank account by giving all the details
            2. Use a negative value as an argument to the withdrawal function
            3. Assert that the withdrawal amount should be non-zero and positive
        """
        account = BankAccount("Harper", 1000)
        withdrawal_amount = -100

        with self.assertRaises(CustomValueError, msg=f"Withdrawal amount must be a non zero positive number"):
            account.withdraw(withdrawal_amount)

    def test_withdrawal_limit(self):
        """
        Test Withdrawal Limit
        This function is used to ensure that the withdrawal amount is not greater than the current balance

        Steps:
            1. Create a bank account by giving all the details
            2. Use a withdrawal amount greater than the current balance as an argument to the withdrawal function
            3. Assert that the withdrawal amount cannot be greater than the current balance
        """
        account = BankAccount("Grey", 1000)
        withdrawal_amount = account.balance + 100

        with self.assertRaises(CustomLimitError, msg=f"Cannot withdraw an amount greater than the account's balance"):
            account.withdraw(withdrawal_amount)

    def test_withdrawal_limit_transaction_limit(self):
        """
        Test Withdrawal Limit Exceeds Transaction Limit
        This function is used to ensure that the withdrawal limit is not greater than the transaction limit
        set on that account.

        Steps:
            1. Create a bank account by giving all the details
            2. Set a transaction limit on the account
            3. Use a withdrawal amount greater than the transaction limit as an argument to the withdrawal function
            4. Assert that the withdrawal amount cannot be greater than the transaction limit

        """
        account = BankAccount("Berlin", 1000)
        account.set_transaction_limit(100)

        with self.assertRaises(CustomLimitError, msg=f"Cannot withdraw amount greater than transaction limit"):
            account.withdraw(200)

    def test_valid_transfer(self):
        """
        Test Valid Transfer

        This function is used to ensure that a valid transfer takes place between two accounts.

        Steps:
            1. Create 2 bank accounts with the right details
            2. transfer amount from first account to second
            3. Ensure that the transfer has happened correctly and raise errors if any
        """
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
        """
        Test Invalid Transfer Type

        Steps:
            1. Create a bank account by giving all the details
            2. Use an incorrect data type as the target bank account to transfer amount
            3. Assert that the target bank account should be an instance of BankAccount
        """
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
