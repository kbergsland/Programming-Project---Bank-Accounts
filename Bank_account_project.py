import random
import functools
from datetime import datetime

class Account:

    def __init__(self, name, account_number, balance):
        self.name = ""
        self.account_number = 0
        self.balance = 0
        self.transaction_counter = 0

    def account_creation(self):
        self.account_number += 1
        self.name = input("Please enter your account name")
        print(f"your account number is: {self.account_number}")
        self.balance = input(int("Please enter your current balance"))

    # Add @get_time decorator to add time functionality to the method
    # Add @transaction_info decorator to display info about the performed transaction
    def deposit(self, deposited_amount):
        self.deposited_amount = 0
        self.deposited_amount += input(int("Please enter your desired deposit."))
        self.balance += self.deposited_amount
        self.transaction_counter += 1
        #Update transaction history with timestamp, transaction type and amount
        #Return transaction_info

    # Add @get_time decorator to add time functionality to the method
    # Add @transaction_info decorator to display info about the performed transaction
    def withdrawal(self, withdrawed_amount):
        self.withdrawed_amount = 0
        self.withdrawed_amount += input(int("Please enter your desired deposit."))
        self.balance += self.withdrawed_amount
        self.transaction_counter += 1
        #Update transaction history with timestamp, transaction type and amount
        #Return transaction_info

    def balance(self):
        return self.balance
    
    def transaction_history(self):
        # history = {time: [transaction_type, amount]}
        pass

    def transaction_history_display(self):
        # 
        pass

    def transaction_info(self):
        pass

    def account_summary(self):
        pass

    def close_account(self):
        pass

    def account_status(self):
        pass

    def timestamp(self):
        time = datetime.now()
        formatted_time = time.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_time



