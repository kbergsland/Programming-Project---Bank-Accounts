import random
import functools
from datetime import datetime

def timestamp(fn):
    def inner():
        time = datetime.now()
        current_time = time.strftime("%d-%m-%Y %H:%M:%S")
        fn(current_time)
    return inner

class Account:

    def __init__(self):
        self.name = ""
        self.account_number = 0
        self.balance = 0.0
        self.transaction_counter = 0
        self.transaction_history = {}
        self.deposited_amount = 0.0
        self.withdrawed_amount = 0.0
        self.closed = True

    def account_creation(self):
        self.account_number += 1
        self.name = input("Please enter your account name")
        print(f"your account number is: {self.account_number:04}")
        self.balance = float(input("Please enter your current balance"))

    @timestamp
    def deposit(self, current_time):
        self.deposited_amount = float(input("Please enter your desired deposit."))
        if self.deposited_amount > 0:
            self.balance += self.deposited_amount
            self.transaction_counter += 1
            self.transaction_history[current_time] = ["Deposit", self.deposited_amount]
            print(f"You deposited {self.deposited_amount} at {current_time}. Your balance is now {self.balance}$.")
        else:
            print("Please enter a positive integer.")

    @timestamp
    def withdrawal(self, current_time):
        self.withdrawed_amount = float(input("Please enter your desired deposit."))
        if self.withdrawed_amount >= self.balance:
            self.balance += self.withdrawed_amount
            self.transaction_counter += 1
            self.transaction_history[current_time] = ["Withdrawal", self.withdrawed_amount]
            print(f"You withdrew {self.deposited_amount} at {current_time}. Your balance is now {self.balance}$.")
        else:
            print("Not enough money in your account")

    def balance(self):
        return self.balance
    
    def transaction_history(self):
        for i in len(self.transaction_history):
            print(self.transaction_history[i])

    def account_summary(self):
        print(f"Account name: {self.name}\nAccount number: {self.account_number:04}\nBalance: {self.balance} \nNumber of transactions: {self.transaction_counter}")

    def close_account(self):
        self.balance = 0


    def account_status(self):
        pass



