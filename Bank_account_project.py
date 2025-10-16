from datetime import datetime

def timestamp(fn):
    def inner(self, *args, **kwargs):
        time = datetime.now()
        current_time = time.strftime("%d-%m-%Y %H:%M:%S")
        fn(self, current_time, *args, **kwargs)
    return inner

def check_balance(fn):
    def inner(self, *args, **kwargs):
        if self.balance <= 0: # når skal denne brukes? mulig vi kun trenger å sjekke saldo ved withdrawal, og sjekke at withdrawal >= balance
            print("Not enough money in your account.")
            return
        else:
            return fn(self, *args, **kwargs)
    return inner

class Account:

    def __init__(self): #(self, name: str, account_number: int, balance: float, transaction_counter: int, transaction_history, deposited_amount: float, withdrawed_amount: float, closed: bool, pin: int)
        self.name = ""
        self.account_number = 0 # burde vi starte på 10000000 for at alle kontoer skal ha 8 siffer?
        self.balance = 0.0 # sjekk at vi får kun 2 desimaler eller om det må kodes inn
        self.transaction_counter = 0
        self.transaction_history = []
        self.deposited_amount = 0.0 # sjekk at vi får kun 2 desimaler eller om det må kodes inn
        self.withdrawn_amount = 0.0 # sjekk at vi får kun 2 desimaler eller om det må kodes inn
        self.closed = False
        self.pin = "" #må ordne at det alltid er 4 digits

    def account_creation(self):
        self.account_number += 1
        self.name = input("Please enter your account name")
        print(f"your account number is: {self.account_number:04}")
        self.balance = float(input("Please enter your current balance"))
        self.pin = int(input("Please enter your desired PIN code"))
        
    def login_info(): # ikke ferdig med denne
        login = self.pin
        pin_input = input("Please enter your PIN code: ")
        for (value) in login.items(): 
            if pin_input == value:
                main()
            else:
                print("\nWrong PIN. Try again.")
                login_info()
        return 

    @timestamp
    def deposit(self, current_time):
        self.deposited_amount = float(input("Please enter your desired deposit."))
        if self.deposited_amount > 0:
            self.balance += self.deposited_amount
            self.transaction_counter += 1
            self.transaction_history.append(current_time, "Deposit: ", f"{self.deposited_amount}$")
            print(f"You deposited {self.deposited_amount} at {current_time}. Your balance is now {self.balance}$.")
        else:
            print("Please enter a positive integer.")

    @timestamp
    @check_balance
    def withdrawal(self, current_time):
        self.withdrawn_amount = float(input("Please enter your desired deposit."))
        self.balance -= self.withdrawn_amount
        self.transaction_counter += 1
        self.transaction_history.append({current_time, "Withdrawal: ", f"{self.withdrawn_amount}$"})
        print(f"You withdrew {self.withdrawn_amount} at {current_time}. Your balance is now {self.balance}$.")

    def get_balance(self):
        return self.balance
    
    def transaction_history(self):
        for i in len(self.transaction_history):
            print(self.transaction_history[i])

    def account_summary(self):
        print(f"Account name: {self.name}\nAccount number: {self.account_number:04}\nBalance: {self.balance} \nNumber of transactions: {self.transaction_counter}")

    def close_account(self):
        self.balance = 0
        self.transaction_history = []
        self.closed = True

    def account_status(self):
        status = input("Please enter your account name.")
        if status == self.name:
            if self.closed == True:
                print("This account has been closed.")
            else:
                print("This account is currently active.")
        else:
            print("No such account.")

    def main(self):

        print("Welcome to the bank. Please choose an option.\n1. ACCESS ACCOUNT\n2. CREATE ACCOUNT\n3. DELETE ACCOUNT\n4. ACCOUNT STATUS")

