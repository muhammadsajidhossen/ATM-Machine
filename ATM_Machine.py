import time
import hashlib
import json
import os

class ATM:
    def __init__(self):
        self.file_name = "users_data.json"
        self.users = self.load_users()
        self.current_users = None 

    def load_users(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as file:
                return json.load(file)
        return {}

    def save_users(self):
        with open(self.file_name, 'w') as file:
            json.dump(self.users, file, indent=4)

    def register(self):
        print("**Register New Account.**")
        account_num = input("Enter Account Number : ")
        if account_num in self.users:
            print("Account number already exists.")
            return
        pin = input("Set a 4-digit PIN : ")
        if len(pin) != 4 or not pin.isdigit():
            print("PIN must be 4 digits.")
            return
        self.users[account_num] = {
            "pin": hashlib.sha256(pin.encode()).hexdigest(),
            "balance": 0,
            "transactions": [],
            "daily_limit": 1000
        }
        self.save_users()
        print(f"Account {account_num} successfully registered.")

    def authenticate(self):
        print("*** Welcome to ATM. ***")
        for _ in range(3):
            account_number = input("Enter Account Number: ")
            pin = input("Enter PIN : ")

            if account_number in self.users:
                hashed_pin = hashlib.sha256(pin.encode()).hexdigest()
                if self.users[account_number]["pin"] == hashed_pin:
                    self.current_users = account_number
                    print("Authentication Successful!")
                    return True
            else:
                print("Incorrect Account Number or PIN. Try again.")
        print("Too many failed attempts. Account locked.")
        return False

    def view_balance(self):
        print(f"Your current balance is : ${self.users[self.current_users]['balance']}")

    def deposit_money(self):
        amount = float(input("Enter amount to deposit : $"))
        if amount <= 0:
            print("Invalid amount.")
            return
        self.users[self.current_users]["balance"] += amount
        self.users[self.current_users]["transactions"].append(f"Deposited : ${amount}")
        self.save_users()
        print(f"Successfully deposited ${amount}")
        print(f"New Balance : ${self.users[self.current_users]['balance']}")

    def withdraw_money(self):
        amount = float(input("Enter amount to Withdraw : $"))
        if (amount <= 0 or
            amount > self.users[self.current_users]['balance'] or
            amount > self.users[self.current_users]['daily_limit']):
            print("Invalid or Exceeded amount.")
            return
        self.users[self.current_users]['balance'] -= amount
        self.users[self.current_users]['transactions'].append(f"Withdraw ${amount}")
        self.save_users()
        print(f"Successfully Withdrew ${amount}")
        print(f"Remaining Balance : ${self.users[self.current_users]['balance']}")

    def view_transactions(self):
        print("Transaction History.")
        transactions = self.users[self.current_users]['transactions']
        print("\n".join(transactions[-5:]) if transactions else "NO Transaction found.")

    def transfer_funds(self):
        recipient = input("Enter recipient account number : ")
        if recipient not in self.users :
            print("Invalid recipient account number.")
            return
            
        if recipient == self.current_users:
            print("You cannot transfer money to your own account.")
            return
        amount = float(input("Enter amount to transfer : $"))
        if amount <= 0 or amount > self.users[self.current_users]['balance']:
            print("Insufficient balance.")
            return
        self.users[self.current_users]['balance'] -= amount
        self.users[recipient]['balance'] += amount
        self.users[self.current_users]['transactions'].append(f"Transferred ${amount} to {recipient}")
        self.save_users()
        print(f"Successfully transferred ${amount} to Account {recipient}")

    def change_pin(self):
        new_pin = input("Enter new 4-digit PIN : ")
        if len(new_pin) == 4 and new_pin.isdigit():
            self.users[self.current_users]['pin'] = hashlib.sha256(new_pin.encode()).hexdigest()
            self.save_users()
            print("PIN changed successfully.")
        else:
            print("PIN must be 4 digits.")

    def main_menu(self):
        while True:
            print("\n**** ATM Menu ****")
            print("1. View Balance")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. View Transactions")
            print("5. Transfer Funds")
            print("6. Change PIN")
            print("7. Exit")
            choice = input("Choose an option: ")
            if choice == "1":
                self.view_balance()
            elif choice == "2":
                self.deposit_money()
            elif choice == "3":
                self.withdraw_money()
            elif choice == "4":
                self.view_transactions()
            elif choice == "5":
                self.transfer_funds()
            elif choice == "6":
                self.change_pin()
            elif choice == "7":
                print("Thank you for using the ATM. Goodbye!")
                break
            else:
                print("Invalid choice. Please select a valid option.")

atm = ATM()
print("1. Register New Account")
print("2. Login")
user_choice = input("Choose an option: ")
if user_choice == "1":
    atm.register()
elif user_choice == "2" and atm.authenticate():
    atm.main_menu()
else:
    print("Exiting ATM system.")
