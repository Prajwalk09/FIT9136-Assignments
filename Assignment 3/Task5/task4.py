# Your code from task 4
from custom_errors import *


class BankAccount:
    account_number = 1045
    opening_bonus = 49.99
    banned_accounts = {}

    @classmethod
    def set_next_account_number(cls, account_number: int) -> None:
        if not isinstance(account_number, int):
            raise CustomTypeError("Account Number must be a number")

        if account_number < 1045:
            raise CustomValueError("Next account number should be at least 1045")

        cls.account_number = account_number

    @classmethod
    def unban_all(cls):
        cls.banned_accounts.clear()

    def __init__(self, owner, balance):
        if not isinstance(owner, str):
            raise CustomTypeError("Owner must be of type string")

        if not owner:
            raise CustomValueError("Owner name cannot be empty")

        if not isinstance(balance, (int, float)):
            raise CustomTypeError("Balance must be a number")

        if balance < 0:
            raise CustomValueError("Balance cannot be less than 0")

        self.owner = owner
        self.balance = balance + self.opening_bonus
        self.account_number = BankAccount.account_number
        BankAccount.account_number += 1
        self.transaction_limit = None
        self.ban_reason = None

        assert self.balance > 0, "Error while initialising balance"
        assert self.account_number >= 1045, "Invalid Account Number"

    def is_banned(self):
        return self.account_number in BankAccount.banned_accounts

    def ban_account(self, reason):
        if not isinstance(reason, str):
            raise CustomTypeError("Reason must be a string")

        BankAccount.banned_accounts[self.account_number] = reason
        self.ban_reason = reason

        assert self.account_number in BankAccount.banned_accounts, "Not banned properly"

    def deposit(self, amount):
        if self.account_number in BankAccount.banned_accounts:
            raise CustomOperationError("Cannot deposit to banned account")

        if not isinstance(amount, (int, float)):
            raise CustomTypeError("Deposit amount should be a number")

        if amount <= 0:
            raise CustomValueError("Deposit amount should be positive")

        current_balance = self.balance
        self.balance += float(amount)

        assert self.balance > current_balance, "Deposit led to decrease in balance"
        assert self.balance >= 0, "Balance became negative after deposit"

    def transfer_to(self, target_account: "BankAccount", amount: float | int) -> None:
        if not isinstance(target_account, BankAccount):
            raise CustomTypeError("Target account must be an object of BankAccount class")

        if self.is_banned() or target_account.is_banned():
            raise CustomOperationError("Cannot transfer to/from banned account")

        if not isinstance(amount, (float, int)):
            raise CustomTypeError("Transfer amount must be a number")

        if amount <= 0:
            raise CustomValueError("Transfer amount must be positive")

        if amount > self.balance:
            raise CustomLimitError("Insufficient funds for transfer")

        if self.transaction_limit is not None and amount > self.transaction_limit:
            raise CustomLimitError("Transfer exceeds transaction limit")

        current_from_balance = self.balance
        current_to_balance = target_account.balance

        self.balance -= amount
        target_account.balance += amount

        assert self.balance < current_from_balance, "Transfer did  not decrease source balance"
        assert target_account.balance > current_to_balance, "Transfer did not increase target balance"
        assert self.balance >= 0, "Source balance is negative after transfer"

    def withdraw(self, amount: float | int) -> None:

        if self.is_banned():
            raise CustomOperationError("Cannot withdraw from a banned account")

        if not isinstance(amount, (int, float)):
            raise CustomTypeError("withdraw amount must be a number")

        if amount <= 0:
            raise CustomValueError("withdraw amount must be positive")

        if amount > self.balance:
            raise CustomLimitError("Insufficient Funds for withdrawal")

        if self.transaction_limit is not None and amount > self.transaction_limit:
            raise CustomLimitError("Withdrawal exceeds transaction limit")

        current_balance = self.balance
        self.balance -= amount
        assert self.balance < current_balance, "withdrawal did not happen correctly"

    def set_transaction_limit(self, limit: float | int | None) -> None:
        if limit is not None:
            if not isinstance(limit, (int, float)):
                raise CustomTypeError("Limit must be a number")
            if limit <= 0:
                raise CustomValueError("Limit must be a positive number")
            self.transaction_limit = limit
        else:
            self.transaction_limit = limit
        assert self.transaction_limit is None or self.transaction_limit > 0, "Transaction Limit not set properly"

    def __str__(self):
        limit_value = "N/A" if self.transaction_limit is None else f"{self.transaction_limit:.2f}"
        banned_str = "Yes" if self.is_banned() else "No"
        banned_reason = f" | Ban Reason: {BankAccount.banned_accounts[self.account_number]}" if self.is_banned() else ""
        return f"{self.owner}'s account ({self.account_number}): Balance=${self.balance:,.2f} | Limit=${limit_value} | "\
               f"Banned={banned_str}{banned_reason}"






