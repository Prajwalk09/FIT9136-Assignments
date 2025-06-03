# Your code from task 4
from custom_errors import *


class BankAccount:
    account_number = 1045
    opening_bonus = 49.99
    banned_accounts = {}

    @classmethod
    def set_next_account_number(cls, account_number: int) -> None:
        """
        This is a class method of the BankAccount class which is used to reset / update what the next account number of
        the BankAccount class is.

        Parameters:
            account_number(int): An integer number denoting the next account number to be reset/update for the
            BankAccount class

        Returns:
            This function does not return anything.
        """
        # If account_number is non-numeric, raise an error
        if not isinstance(account_number, int):
            raise CustomTypeError("Account Number must be a number")

        # If account_number is less than 1045, raise an error.
        if account_number < 1045:
            raise CustomValueError("Next account number should be at least 1045")

        # Set the class variable account_number to the account_number given as input.
        cls.account_number = account_number

    @classmethod
    def unban_all(cls) -> None:
        """
        This is a class method which is used to unban all the accounts of the BankAccount class.

        Parameters:
            This function does not take any inputs.
        Returns:
            This function does not return anything. It just clears the class variable banned_accounts.
        """
        # unbanning all the accounts.
        cls.banned_accounts.clear()

    def __init__(self, owner: str, balance: int | float) -> None:
        """
        This is the constructor of the BankAccount class. It is used to initialise values to an object, every time
        an object is created.

        Parameters:
            owner(str): A value of type string which signifies the name of the owner of the BankAccount
            balance(int|float): A numeric value signifying the initial balance of the account.
        """
        # If the type of owner name is not a string, raise an error
        if not isinstance(owner, str):
            raise CustomTypeError("Owner must be of type string")

        # If owner name is empty, raise an error
        if not owner:
            raise CustomValueError("Owner name cannot be empty")

        # If balance is non-numeric, raise an error
        if not isinstance(balance, (int, float)):
            raise CustomTypeError("Balance must be a number")

        # If balance is negative, raise an error
        if balance < 0:
            raise CustomValueError("Balance cannot be less than 0")

        # If the balance is 0, raise an error
        if balance == 0:
            raise CustomValueError("Balance should be positive and greater than 0")

        # Setting the owner name, account balance (initial balance + joining bonus), account_number
        self.owner = owner
        self.balance = balance + self.opening_bonus
        self.account_number = BankAccount.account_number
        BankAccount.account_number += 1

        # No transaction limit initially. Can be explicitly set later. Same holds good for ban_reason as well.
        self.transaction_limit = None
        self.ban_reason = None

        # Check for positive balance and account number being at least 1045.
        assert self.balance > 0, "Error while initialising balance"
        assert self.account_number >= 1045, "Invalid Account Number"

    def is_banned(self) -> bool:
        """
        This is a function which is used to check if the instance of BankAccount calling this function has been banned
        or not. It does it by checking if the account number of the instance calling the function is in
        the banned_accounts class variable.

        Returns:
            This function returns a boolean value describing whether the account has been banned or not.
        """
        return self.account_number in BankAccount.banned_accounts

    def ban_account(self, reason:str) -> None:
        """
        This function is used to ban the account of the instance calling this function. This function takes only
        one input. The reason for banning the account.

        Parameters:
            reason(str): A string value which contains the reason for banning that particular account
        Returns:
            This function does not return anything.
        """
        # If reason is not a string, raise an error
        if not isinstance(reason, str):
            raise CustomTypeError("Reason must be a string")

        # Update the banned_accounts dictionary with the bank account number and the reason for the ban.
        BankAccount.banned_accounts[self.account_number] = reason
        self.ban_reason = reason

        # Ensuring the account number is the banned_accounts dict.
        assert self.account_number in BankAccount.banned_accounts, "Not banned properly"

    def deposit(self, amount: int|float) -> None:
        """
        This function is used to deposit an amount to the bank account of the instance calling this function.

        Parameters:
            amount (int|float): This function takes a numeric input for the amount which has to be deposited.

        Returns:
              This function does not return anything. It just updates the bank account of the instance calling
              this function.
        """
        # If the bank account is banned, raise an error signifying transfer not possible
        if self.account_number in BankAccount.banned_accounts:
            raise CustomOperationError("Cannot deposit to banned account")

        # If the amount to be deposited is non-numeric, raise an error
        if not isinstance(amount, (int, float)):
            raise CustomTypeError("Deposit amount should be a number")

        # If the amount is either negative or zero, raise an error
        if amount <= 0:
            raise CustomValueError("Deposit amount should be positive")

        # Keep track of current balance and update the balance
        current_balance = self.balance
        self.balance += float(amount)

        # Check if the balance has been correctly updated and also that the balance is non-negative after deposit
        assert self.balance > current_balance, "Deposit led to decrease in balance"
        assert self.balance >= 0, "Balance became negative after deposit"

    def transfer_to(self, target_account: "BankAccount", amount: float | int) -> None:
        """
        This function is used to transfer an amount from one bank account to another bank account. This function takes
        the target bank account and the amount to be transferred as inputs.

        Parameters:
            target_account(BankAccount): An instance of the BankAccount type which signifies the target bank account
                                         to which funds have to be transferred from the source bank account.
            amount(int|float): A numeric value expressing the amount to be transferred.

        Returns:
            This function does not return anything.
        """
        # If the target_account is not an instance of BankAccount, raise an error
        if not isinstance(target_account, BankAccount):
            raise CustomTypeError("Target account must be an object of BankAccount class")

        # If either the source or the target_account is banned, raise an error
        if self.is_banned() or target_account.is_banned():
            raise CustomOperationError("Cannot transfer to/from banned account")

        # If the amount to be transferred is non-numeric, raise an error
        if not isinstance(amount, (float, int)):
            raise CustomTypeError("Transfer amount must be a number")

        # If the amount is either 0 or negative, raise an error
        if amount <= 0:
            raise CustomValueError("Transfer amount must be positive")

        # If the amount to be transferred is greater than the existing balance of the source account, raise an error
        if amount > self.balance:
            raise CustomLimitError("Insufficient funds for transfer")

        # If the amount to be transferred is greater than the transaction limit for the source account, raise an error
        if self.transaction_limit is not None and amount > self.transaction_limit:
            raise CustomLimitError("Transfer exceeds transaction limit")

        # Keep track of the current balance of source account and target accounts.
        current_from_balance = self.balance
        current_to_balance = target_account.balance

        # Deduct amount from source and add it to target
        self.balance -= amount
        target_account.balance += amount

        """
        Ensure the source balance after deduction is lesser than previous balance and target balance after the
        transfer is higher than the greater than the previous balance and also ensure that the source balance is in
        positive after the transfer.
        """

        assert self.balance < current_from_balance, "Transfer did  not decrease source balance"
        assert target_account.balance > current_to_balance, "Transfer did not increase target balance"
        assert self.balance >= 0, "Source balance is negative after transfer"

    def withdraw(self, amount: float | int) -> None:
        """
        This function is used to withdraw funds from the bank account of the instance calling this function.
        This function takes the amount to be withdrawn as input.

        Parameters:
            amount(int|float): A numeric value expressing the amount to be withdrawn from the account.

        Returns:
            This function does not return anything.
        """
        # If the account is banned, raise an error
        if self.is_banned():
            raise CustomOperationError("Cannot withdraw from a banned account")

        # If the amount is non-numeric raise an error
        if not isinstance(amount, (int, float)):
            raise CustomTypeError("withdraw amount must be a number")

        # If the amount is zero or negative, raise an error
        if amount <= 0:
            raise CustomValueError("withdraw amount must be positive")

        # If the amount to be withdrawn is greater than the existing balance, raise an error
        if amount > self.balance:
            raise CustomLimitError("Insufficient Funds for withdrawal")

        # If the amount to be withdrawn is greater than the transaction limit set for the account, raise an error
        if self.transaction_limit is not None and amount > self.transaction_limit:
            raise CustomLimitError("Withdrawal exceeds transaction limit")

        # Keep track of the current account balance and deduct the amount from the account
        current_balance = self.balance
        self.balance -= amount

        # Ensure the new balance after deduction is lesser than the old balance before deduction.
        assert self.balance < current_balance, "withdrawal did not happen correctly"

    def set_transaction_limit(self, limit: float | int | None) -> None:
        """
        This function is used to set a transaction limit on the bank account of the instance calling this function. This
        function takes the transaction limit to be set as input.

        Parameters:
            limit(int|float|None): A value of type int, float or None which signifies the transaction limit to be set
                                   on the bank account of the instance calling this function.

        Returns:
            This function does not return anything.
        """
        # If the limit is None, execute this block
        if limit is not None:
            # If the type of the transaction limit is non-numeric, raise an error
            if not isinstance(limit, (int, float)):
                raise CustomTypeError("Limit must be a number")

            # If the value of the transaction limit is zero or non-negative, raise an error
            if limit <= 0:
                raise CustomValueError("Limit must be a positive number")

            # Set the transaction limit
            self.transaction_limit = limit
        else:
            self.transaction_limit = limit

        # Ensure that the limit has been set properly
        assert self.transaction_limit is None or self.transaction_limit > 0, "Transaction Limit not set properly"

    def __str__(self):
        """
        This is a dunder (double underscore) function which is used to display the object of the BankAccount class
        and it's attributes

        Parameters:
            This function does not take any inputs.
        Returns:
            This function does not return anything.
        """
        limit_value = "N/A" if self.transaction_limit is None else f"{self.transaction_limit:.2f}"
        banned_str = "Yes" if self.is_banned() else "No"
        banned_reason = f" | Ban Reason: {BankAccount.banned_accounts[self.account_number]}" if self.is_banned() else ""

        # Return a formatted f-string
        return f"{self.owner}'s account ({self.account_number}): Balance=${self.balance:,.2f} | Limit=${limit_value} | " \
               f"Banned={banned_str}{banned_reason}"
