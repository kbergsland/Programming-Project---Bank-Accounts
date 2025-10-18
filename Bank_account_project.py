# -*- coding: utf-8 -*-
"""
Created on Sat Oct 18 12:52:27 2025

@author: T-Skrrt
"""

from datetime import datetime

def timestamp(fn):
    def inner(self, *args, **kwargs):
        time = datetime.now()
        current_time = time.strftime("%d-%m-%Y %H:%M:%S")
        return fn(self, current_time, *args, **kwargs)
    return inner

class BankAccount:

    def __init__(self):
        self.name = ""
        self.account_number = 10000000
        self.balance = 0.0
        self.transaction_counter = 0
        self.transaction_history = []  # list of tuples: (time, type, amount)
        self.closed = False
        self.pin = ""  # as string
        self.logged_in = False

    def account_creation(self):
        self.account_number += 1
        self.name = input("Please enter your name: ").strip()
        print(f"Your account number is: {self.account_number:04}")
        while True:
            try:
                initial_balance = float(input("Please enter your current balance: "))
                if initial_balance < 0:
                    print("Initial balance cannot be negative.")
                    continue
                self.balance = round(initial_balance, 2)
                break
            except ValueError:
                print("Please enter a valid number for balance.")
        while True:
            pin_input = input("Please enter your desired 4-digit PIN code: ").strip()
            if pin_input.isdigit() and len(pin_input) == 4:
                self.pin = pin_input
                break
            else:
                print("PIN must be exactly 4 digits.")
        print(30*"-", "\nAccount created successfully!\n", 30*"-")

    def login_info(self, user_info, valid_users):
        username, pin = user_info
        return username in valid_users and pin == valid_users[username]

    def login(self):
        if self.closed:
            print("This account is closed — you cannot login.")
            return False

        valid_users = { self.name : self.pin }
        name_input = input("Please enter your name: ").strip()
        pin_input = input("Enter PIN: ").strip()
        if self.login_info((name_input, pin_input), valid_users):
            self.logged_in = True
            print("Login successful.")
            return True
        else:
            print("Invalid name or PIN.")
            return False

    @timestamp
    def deposit(self, current_time):
        if not self.logged_in:
            print("You must be logged in to deposit.")
            return
        try:
            amount = float(input("Please enter your desired deposit amount: "))
        except ValueError:
            print("Please enter a valid number.")
            return
        if amount <= 0:
            print("Please enter a positive amount.")
            return
        amount = round(amount, 2)
        self.balance += amount
        self.balance = round(self.balance, 2)
        self.transaction_counter += 1
        self.transaction_history.append((current_time, "Deposit", f"{amount}$"))
        print(f"You deposited {amount}$ at {current_time}. Your balance is now {self.balance}$.")

    @timestamp
    def withdraw(self, current_time):
        if not self.logged_in:
            print("You must be logged in to withdraw.")
            return
        try:
            amount = float(input("Please enter your desired withdrawal amount: "))
        except ValueError:
            print("Please enter a valid number.")
            return
        if amount <= 0:
            print("Please enter a positive amount.")
            return
        if amount > self.balance:
            print(30*"-", "Not enough money in your account.", 30*"-")
            return
        amount = round(amount, 2)
        self.balance -= amount
        self.balance = round(self.balance, 2)
        self.transaction_counter += 1
        self.transaction_history.append((current_time, "Withdrawal", f"{amount}$"))
        print(f"You withdrew {amount}$ at {current_time}. Your balance is now {self.balance}$.")

    def show_balance(self):
        if not self.logged_in:
            print("You must be logged in to view balance.")
            return
        print(f"Balance for {self.name}: {self.balance:.2f}$")

    def show_transaction_history(self):
        if not self.logged_in:
            print("You must be logged in to view transaction history.")
            return
        if len(self.transaction_history) == 0:
            print("No transactions yet.")
            return
        print("\nTransaction history:")
        for entry in self.transaction_history:
            time, kind, amount = entry
            print(f"{time} | {kind} | {amount}")
        print("")

    def account_summary(self):
        if not self.logged_in:
            print("You must be logged in to view account summary.")
            return
        print(30*"-")
        print(f"Account name: {self.name}")
        print(f"Account number: {self.account_number:04}")
        print(f"Balance: {self.balance:.2f}$")
        print(f"Number of transactions: {self.transaction_counter}")
        print(30*"-")

    def close_account(self):
        if not self.logged_in:
            print("You must be logged in to close account.")
            return
        self.balance = 0.0
        self.transaction_history = []
        self.closed = True
        print("Your account has been closed.")

    def account_status(self):
        name_check = input(f"{30*'-'}\nPlease enter your account name:\n{30*'-'}\n").strip()
        if name_check == self.name:
            if self.closed:
                print(30*"*", "This account has been closed.", 30*"*")
            else:
                print(30*"*", "This account is currently active.", 30*"*")
        else:
            print(30*"*", "\nAccount not found.\n", 30*"*")

    def main_menu(self):
        print(30*"-", "\nMAIN MENU\n", 30*"-",
              "\n1. Access account\n2. Create Account\n3. Close account\n4. Account status\n5. Quit\n", 30*"-")

    def account_menu(self):
        print(30*"-", "\nACCOUNT MENU\n", 30*"-",
              "\n1. Withdraw money\n2. Deposit money\n3. Transaction history\n4. Account summary\n5. Return to main menu\n", 30*"-")

def main():
    run_program = True
    account = None  # hold current account
    while run_program:
        if account is None:
            account = BankAccount()
        account.main_menu()
        try:
            mainmenu_choice = int(input("Enter your number of choice from the menu (1-5): ").strip())
        except ValueError:
            print("Invalid input. Please choose a number between 1 and 5.")
            continue

        if mainmenu_choice == 1:
            if account.login():
                while True:
                    account.account_menu()
                    try:
                        accountmenu_choice = int(input("Enter your number of choice from the menu (1-5): ").strip())
                    except ValueError:
                        print("Invalid input. Please choose a number between 1 and 5.")
                        continue

                    if accountmenu_choice == 1:
                        account.withdraw()
                    elif accountmenu_choice == 2:
                        account.deposit()
                    elif accountmenu_choice == 3:
                        account.show_transaction_history()
                    elif accountmenu_choice == 4:
                        account.account_summary()
                    elif accountmenu_choice == 5:
                        break
                    else:
                        print("Invalid input. Please choose a number between 1 and 5.")
            else:
                # login failed
                continue

        elif mainmenu_choice == 2:
            account = BankAccount()  # ny konto
            account.account_creation()

        elif mainmenu_choice == 3:
            if account.login():
                account.close_account()
            else:
                continue

        elif mainmenu_choice == 4:
            account.account_status()

        elif mainmenu_choice == 5:
            print("Goodbye!")
            run_program = False

        else:
            print("Invalid input. Please choose a number between 1 and 5.")

if __name__ == "__main__":
    main()

