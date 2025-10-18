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
            print(30*"-","Not enough money in your account.",30*"-")
            return
        else:
            return fn(self, *args, **kwargs)
    return inner

class BankAccount:

    def __init__(self):
        self.name = ""
        self.account_number = 10000000
        self.balance = 0.0 # sjekk at vi får kun 2 desimaler eller om det må kodes inn
        self.transaction_counter = 0
        self.transaction_history = []
        self.deposited_amount = 0.0 # sjekk at vi får kun 2 desimaler eller om det må kodes inn
        self.withdrawn_amount = 0.0 # sjekk at vi får kun 2 desimaler eller om det må kodes inn
        self.closed = False
        self.pin = "" #må være 4 digits
        #self.logged_in = False # denne tester jeg om fikser login

    def account_creation(self):
        self.account_number += 1
        self.name = input("Please enter your name: ")
        print(f"your account number is: {self.account_number:04}")
        self.balance = float(input("Please enter your current balance: "))
        self.pin = int(input("Please enter your desired PIN code: "))
        print(30*"-","\nAccount created successfully!\n",30*"-")
        
    def login_info(self, user_info, valid_users):
        if user_info[0] in valid_users:
            if user_info[1] == valid_users[user_info[0]]:
                return True
        else:
            return False
        
    def login(self):
        valid_users = {self.name:self.pin}
        while True:
            print()
            name_input = input("Please enter your name: ")
            pin_input = input("Enter PIN: ")
            user_info = (name_input, pin_input)
            if self.login_info(user_info, valid_users):
                #self.logged_in = True # kanskje denne hjelper
                print("Login successful.")
                return True
            else:
                print("Invalid name or PIN.") #hvorfor dukker denne opp
                return False

    @timestamp
    def deposit(self, current_time):
        self.deposited_amount = float(input("Please enter your desired deposit."))
        if self.deposited_amount > 0:
            self.balance += self.deposited_amount
            self.transaction_counter += 1
            self.transaction_history.append(current_time, "Deposit: ", f"{self.deposited_amount}$")
            print(f"You deposited {self.deposited_amount} at {current_time}. Your balance is now {self.balance}$.")
        else:
            print(30*"-","Please enter a positive integer.",30*"-")

    @timestamp
    @check_balance
    def withdraw(self, current_time):
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
        status = input(30*"-", "\nPlease enter your account name.\n",30*"-")
        if status == self.name:
            if self.closed == True:
                print(30*"*","This account has been closed.",30*"*")
            else:
                print(30*"*","This account is currently active.",30*"*")
        else:
            print(30*"*","\nAccount not found.\n",30*"*")
            
    def main_menu(self):
            print(30*"-","\nMAIN MENU\n",30*"-","\n1. Access account\n2. Create Account\n3. Close account\n4. Account status\n5. Quit\n",30*"-")

    def account_menu(self):
            print(30*"-","\nACCOUNT MENU\n",30*"-","\n1. Withdraw money\n2. Deposit money\n3. Transaction history\n4. Account summary\n5. Return to main menu\n",30*"-")
            
def main():
    run_program = True
    while run_program:
        account = BankAccount()
        account.main_menu()
        mainmenu_choice = int(input("Enter your number of choice from the menu (1-5):"))
        if mainmenu_choice == 1:
            account.login()
            if account.login_info == True:
                account.account_menu()
                accountmenu_choice = int(input("Enter your number of choice from the menu (1-5):"))
                if accountmenu_choice == 1:
                    account.withdraw()
                elif accountmenu_choice == 2:
                    account.deposit()
                elif accountmenu_choice == 3:
                    account.transaction_history()
                elif accountmenu_choice == 4:
                    account.account_summary()
                elif accountmenu_choice == 5:
                    account.main_menu()
                else:
                    print("Invalid input. Please choose a number between 1 and 5.")
            else:
                print("Wrong PIN. Try again") # denne kommer opp
                account.login()
        elif mainmenu_choice == 2:
            account.account_creation()
        elif mainmenu_choice == 3:
            account.login()
            if account.correct_pin == True:
                print("Your account was closed successfully.")
                account.close_account()
                account.main_menu()
            else:
                account.main_menu()
        elif mainmenu_choice == 4:
            account.account_status()
        elif mainmenu_choice == 5:
            print("Goodbye!")
            run_program == False
        else:
            print("Invalid input. Please choose a number between 1 and 5.")
    
main()
    
    
                    
