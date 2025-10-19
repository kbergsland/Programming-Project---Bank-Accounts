
from datetime import datetime

#alt likt
def timestamp(fn):
    def inner(self, *args, **kwargs):
        now = datetime.now()
        current_time = now.strftime("%d-%m-%Y %H:%M:%S")
        return fn(self, current_time, *args, **kwargs)
    return inner

def check_balance(fn):
    """Validate that the *withdrawn amount argument* is positive and <= balance.
    Works regardless of decorator order by inspecting args/kwargs."""
    def inner(self, *args, **kwargs):
        # Try to get 'withdrawn_amount' from kwargs first
        amount = kwargs.get("withdrawn_amount", None)

        # Otherwise, try positional args. Our withdraw signature is:
        #   withdraw(self, current_time, withdrawn_amount)
        # After timestamp, args should be (current_time, withdrawn_amount)
        if amount is None:
            if len(args) >= 2 and isinstance(args[1], (int, float)):
                amount = args[1]
            elif len(args) >= 1 and isinstance(args[0], (int, float)):
                amount = args[0]

        if amount is None:
            print(30*"-", "\nNo withdrawal amount provided.\n", 30*"-")
            return

        if amount > self.balance:
            print(30*"-", "\nNot enough money in your account.\n", 30*"-")
            return
        if amount <= 0:
            print(30*"*", "\nPlease enter a positive amount.\n", 30*"*")
            return

        return fn(self, *args, **kwargs)
    return inner

# ----------------------------
# BankAccount
# ----------------------------
class BankAccount:
    _registry = []         # All accounts
    _next_account = 10000001

    def __init__(self):
        self.name = ""
        self.account_number = None
        self.balance = 0.0
        self.transaction_counter = 0
        self.transaction_history = []
        self.closed = False
        self.pin = ""              # 4-digit string
        self.logged_in = False

    def account_creation(self):
        # Assign unique account number
        self.account_number = type(self)._next_account
        type(self)._next_account += 1

        self.name = input("Please enter your name: ").strip()

        # Initial balance
        while True:
            try:
                initial_balance = float(input("Please enter your current balance: "))
                if initial_balance < 0:
                    print(30*"*", "\nInitial balance cannot be negative.\n", 30*"*")
                    continue
                self.balance = round(initial_balance, 2)
                break
            except ValueError:
                print(30*"*", "\nPlease enter a valid number.\n", 30*"*")

        # PIN
        while True:
            pin_input = input("Please choose a 4-digit PIN: ").strip()
            if pin_input.isdigit() and len(pin_input) == 4:
                self.pin = pin_input
                break
            else:
                print(30*"*", "\nPIN must be exactly 4 digits.\n", 30*"*")
        type(self)._registry.append(self)
        print(30*"-", f"\nYour account number is: {self.account_number}\n", 30*"-")
        print(30*"*", "\nAccount created successfully!\n", 30*"*")

    # ---------- Auth ----------
    @classmethod
    def _find_by_number_and_pin(cls, number, pin):
        for acc in cls._registry:
            if not acc.closed and acc.account_number == number and acc.pin == pin:
                return acc
        return None

    @classmethod
    def _find_by_name_and_pin(cls, name, pin):
        for acc in cls._registry:
            if not acc.closed and acc.name == name and acc.pin == pin:
                return acc
        return None

    @classmethod
    def login(cls):
        ident = input("Enter account number OR name: ").strip()
        pin = input("Enter PIN: ").strip()

        # Prefer account number when numeric
        if ident.isdigit():
            acc = cls._find_by_number_and_pin(int(ident), pin)
        else:
            acc = cls._find_by_name_and_pin(ident, pin)

        if acc:
            acc.logged_in = True
            print("\nLogin successful.\n")
            return acc
        else:
            print(30*"*", "\nInvalid name or PIN.\n", 30*"*")
            return None

    # ---------- Operations ----------
    @timestamp
    def deposit(self, current_time):
        try:
            deposited_amount = float(input("Please enter your desired deposit amount ($): "))
        except ValueError:
            print(30*"*", "\nPlease enter a valid number.\n", 30*"*")
            return
        if deposited_amount <= 0:
            print(30*"*", "\nPlease enter a positive amount.\n", 30*"*")
            return

        deposited_amount = round(deposited_amount, 2)
        self.balance = round(self.balance + deposited_amount, 2)
        self.transaction_counter += 1
        self.transaction_history.append(
            {"time": current_time, "type": "Deposit", "amount": deposited_amount}
        )
        print(30*"*", f"\nYou deposited {deposited_amount}$ at {current_time}. "
                      f"Your balance is now {self.balance}$.\n", 30*"*")

    @timestamp
    @check_balance
    def withdraw(self, current_time, withdrawn_amount):
        withdrawn_amount = round(withdrawn_amount, 2)
        self.balance = round(self.balance - withdrawn_amount, 2)
        self.transaction_counter += 1
        self.transaction_history.append(
            {"time": current_time, "type": "Withdrawal", "amount": withdrawn_amount}
        )
        print(30*"*", f"\nYou withdrew {withdrawn_amount}$ at {current_time}. "
                      f"Your balance is now {self.balance}$.\n", 30*"*")

    # ---------- Info ----------
    def show_balance(self):
        print(30*"*", f"\nBalance for {self.name}: {self.balance:.2f}$\n", 30*"*")

    def show_transaction_history(self):
        if not self.transaction_history:
            print(30*"*", "\nNo transactions yet.\n", 30*"*")
            return
        print(30*"*", "\nTransaction history:\n")
        for tr in self.transaction_history:
            print(f"{tr['time']} | {tr['type']} | {tr['amount']}$")
        print(30*"*")

    def account_summary(self):
        print(30*"-")
        print(f"Account name: {self.name}")
        print(f"Account number: {self.account_number}")
        print(f"Balance: {self.balance:.2f}$")
        print(f"Number of transactions: {self.transaction_counter}")
        print(30*"-")

    def close_account(self):
        self.balance = 0.0
        self.transaction_history = []
        self.closed = True
        print(30*"*", "\nYour account has been closed.\n", 30*"*")

    @classmethod
    def account_status(cls):
        ident = input(f"{30*'-'}\nEnter account number OR name to check status:\n{30*'-'}\n").strip()
        acc = None
        if ident.isdigit():
            for a in cls._registry:
                if a.account_number == int(ident):
                    acc = a
                    break
        else:
            for a in cls._registry:
                if a.name == ident:
                    acc = a
                    break
        if acc is None:
            print(30*"*", "\nAccount not found.\n", 30*"*")
            return
        if acc.closed:
            print(30*"*", "This account has been closed.", 30*"*")
        else:
            print(30*"*", "This account is currently active.", 30*"*")

# ----------------------------
# Menus (free functions)
# ----------------------------
def print_main_menu():
    print(30*"-", "\nMAIN MENU\n", 30*"-",
          "\n1. Access account\n2. Create Account\n3. Close account\n4. Account status\n5. Quit\n", 30*"-")

def print_account_menu():
    print(30*"-", "\nACCOUNT MENU\n", 30*"-",
          "\n1. Withdraw money\n2. Deposit money\n3. Transaction history\n4. Account summary\n5. Return to main menu\n", 30*"-")

# ----------------------------
# Main
# ----------------------------
def main():
    run_program = True
    while run_program:
        print_main_menu()
        try:
            main_choice = int(input("Enter your number of choice from the menu (1-5): ").strip())
        except ValueError:
            print(30*"*", "\nInvalid input. Please choose a number between 1 and 5.\n", 30*"*")
            continue

        if main_choice == 1:
            current = BankAccount.login()
            if not current:
                continue
            # Account menu loop
            while True:
                print_account_menu()
                try:
                    acct_choice = int(input("Enter your number of choice from the menu (1-5): ").strip())
                except ValueError:
                    print(30*"*", "\nInvalid input. Please choose a number between 1 and 5.\n", 30*"*")
                    continue

                if acct_choice == 1:
                    try:
                        amt = float(input("Please enter your desired withdrawal amount: "))
                    except ValueError:
                        print(30*"*", "\nPlease enter a valid number.\n", 30*"*")
                        continue
                    current.withdraw(amt)

                elif acct_choice == 2:
                    current.deposit()

                elif acct_choice == 3:
                    current.show_transaction_history()

                elif acct_choice == 4:
                    current.account_summary()

                elif acct_choice == 5:
                    print("\nReturning to main menu...\n")
                    break

                else:
                    print(30*"*", "\nInvalid input. Please choose a number between 1 and 5.\n", 30*"*")

        elif main_choice == 2:
            acc = BankAccount()
            acc.account_creation()

        elif main_choice == 3:
            acc = BankAccount.login()
            if acc:
                acc.close_account()

        elif main_choice == 4:
            BankAccount.account_status()

        elif main_choice == 5:
            print(30*"*", "\nGoodbye!\n", 30*"*")
            run_program = False

        else:
            print(30*"*", "\nInvalid input. Please choose a number between 1 and 5.\n", 30*"*")

if __name__ == "__main__":
    main()
