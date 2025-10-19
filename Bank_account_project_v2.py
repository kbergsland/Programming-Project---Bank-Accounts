from datetime import datetime

def timestamp(fn):
    def inner(self, *args, **kwargs):
        time = datetime.now()
        current_time = time.strftime("%d-%m-%Y %H:%M:%S")
        return fn(self, current_time, *args, **kwargs)
    return inner

def check_balance(fn):
    def inner(self, *args, **kwargs):
        if self.balance <= 0:
            print(30*"-", "Not enough money in your account.", 30*"-")
            return
        else:
            return fn(self, *args, **kwargs)
    return inner

class Account:
    def __init__(self):
        self.name = ""
        self.account_number = 10000000
        self.balance = 0.0
        self.transaction_counter = 0
        self.transaction_history = []
        self.deposited_amount = 0.0
        self.withdrawn_amount = 0.0
        self.closed = False
        self.pin = ""

    def account_creation(self):
        self.account_number += 1
        self.name = input("Please enter your name: ")
        print(f"Your account number is: {self.account_number:04}")
        self.balance = float(input("Please enter your current balance: "))
        self.pin = input("Please enter your desired 4-digit PIN code: ")
        while len(self.pin) != 4 or not self.pin.isdigit():
            self.pin = input("PIN must be exactly 4 digits. Please try again: ")
        print(30*"-", "\nAccount created successfully!\n", 30*"-")

    def login_info(self, user_info, valid_users):
        username, pin = user_info
        return valid_users.get(username) == pin

    def login(self):
        valid_users = {self.name: self.pin}
        name_input = input("Please enter your name: ")
        pin_input = input("Enter PIN: ")
        user_info = (name_input, pin_input)
        if self.login_info(user_info, valid_users):
            print("Login successful.")
            return True
        else:
            print("Invalid name or PIN.")
            return False

    @timestamp
    def deposit(self, current_time):
        try:
            self.deposited_amount = float(input("Please enter your desired deposit: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            return
        if self.deposited_amount > 0:
            self.balance += self.deposited_amount
            self.transaction_counter += 1
            self.transaction_history.append({
                "time": current_time,
                "type": "Deposit",
                "amount": round(self.deposited_amount, 2)
            })
            print(f"You deitposed {self.deposited_amount}$ at {current_time}. Your balance is now {self.balance}$.")
        else:
            print(30*"-", "Please enter a positive amount.", 30*"-")

    @timestamp
    @check_balance
    def withdraw(self, current_time):
        try:
            self.withdrawn_amount = float(input("Please enter your desired withdrawal: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            return
        if self.withdrawn_amount <= self.balance:
            self.balance -= self.withdrawn_amount
            self.transaction_counter += 1
            self.transaction_history.append({
                "time": current_time,
                "type": "Withdrawal",
                "amount": round(self.withdrawn_amount, 2)
            })
            print(f"You withdrew {self.withdrawn_amount}$ at {current_time}. Your balance is now {self.balance}$.")
        else:
            print("Not enough funds for this withdrawal.")

    def get_balance(self):
        print(f"Your current balance is: {self.balance}$")

    def show_transaction_history(self):
        if not self.transaction_history:
            print("No transactions yet.")
        else:
            print(30*"-", "TRANSACTION HISTORY", 30*"-")
            for i in self.transaction_history:
                print(f"{i['time']} - {i['type']}: {i['amount']}$")

    def account_summary(self):
        print(30*"-", "\nACCOUNT SUMMARY\n", 30*"-")
        print(f"Account name: {self.name}")
        print(f"Account number: {self.account_number:04}")
        print(f"Balance: {self.balance}$")
        print(f"Number of transactions: {self.transaction_counter}")

    def close_account(self):
        self.balance = 0
        self.transaction_history.clear()
        self.closed = True
        print("Your account has been closed.")

    def account_status(self):
        status = input(f"{30*'-'}\nPlease enter your account name.\n{30*'-'}\n")
        if status == self.name:
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
    account = Account()
    run_program = True
    while run_program:
        account.main_menu()
        try:
            mainmenu_choice = int(input("Enter your number of choice from the menu (1-5): "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        if mainmenu_choice == 1:
            if account.login():
                while True:
                    account.account_menu()
                    try:
                        accountmenu_choice = int(input("Enter your number of choice from the menu (1-5): "))
                    except ValueError:
                        print("Invalid input. Please enter a number.")
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
        elif mainmenu_choice == 2:
            account.account_creation()
        elif mainmenu_choice == 3:
            if account.login():
                account.close_account()
        elif mainmenu_choice == 4:
            account.account_status()
        elif mainmenu_choice == 5:
            print("Goodbye!")
            run_program = False
        else:
            print("Invalid input. Please choose a number between 1 and 5.")

if __name__ == "__main__":
    main()
