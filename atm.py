#FINAL PROJECT:ATM SYSTEM.
import datetime #For adding timestamps with actions
import json     #For saving the transaction(Actions) history
import random   #For generating account numbers for different users

class ATM:
  def __init__(self):
    self.accounts={}
    self.current_user=None
    try:
      with open("accounts_data.json","r") as f:
        self.accounts=json.load(f)
    except FileNotFoundError:
      self.accounts={}

# Adding Timestamps with actions:
  def add_timestamp(self):
    presenthour=datetime.datetime.now().strftime("%d/%m/%Y  %H:%M:%S")
    return presenthour

# Saving data to JSON File
  def save_data(self):
    with open("accounts_data.json","w") as save:
      json.dump(self.accounts,save,indent=4)


# Authentication:
  def authenticate(self):
    print("\n===== USER LOGIN =====")
    acc_num = input("Enter Account Number: ")
    
    
    # Step A: Validate if the account key exists in our dictionary
    if acc_num not in self.accounts:
      print("Invalid Account Number or PIN.")
      return False
    
    
    # Step B: If account exists, verify the PIN
    attempts=3
    stored_pin = self.accounts[acc_num]["PIN"]

    while attempts>0:
      while True:
        entered_pin=input("Enter Your 4-Digit PIN:")
        if len(entered_pin)==4 and entered_pin.isdigit():
          break
        print("\nInvalid PIN!\nPIN must be of 4-Digits.")

      if (entered_pin==stored_pin):
        # Step C: Establish the global active session!
        self.current_user = acc_num
        print(f"\nWelcome back, {self.accounts[acc_num]['Name']}!")
        print("\nLogin Successful.")
        return True
      else:
        attempts-=1
        print(f"Incorrect Pin.\nAttempts Left:{attempts}")

    print("\nToo many wrong Attempts.")
    return False

# Create New Account
  def create_account(self):
    print("\n=====Create New Account=====")
    name=input("Enter Your Full Name:")

    while True:
      pin=input("Create 4-Digit PIN:")
      if len(pin)==4 and pin.isdigit():
        break
      print("\nInvalid PIN!\nMust be exactly 4-Digits.")
    
    while True:
      new_acc_num=str(random.randint(1000,9999))
      if new_acc_num not in self.accounts:
        break
    
    self.accounts[new_acc_num]={
      "Name":name,
      "PIN":pin,
      "Balance":0.0,
      "Mini-Statement":[f"Account Created on {self.add_timestamp()}"]
    }
    self.save_data()
    print(f"Account Created Successfully.\nYour Account Number is:{new_acc_num}.\nPlease remember this number to login.")
                      
# Check Balance:
  def check_balance(self):
    current_bal=self.accounts[self.current_user]["Balance"]
    print(f"\nCurrent Balance:Rs.{current_bal:.2f}\n{self.add_timestamp()}")
    self.accounts[self.current_user]["Mini-Statement"].append(
        f"Check Balance -> Rs.{current_bal:.2f}   {self.add_timestamp()}"
    )

# Deposit Money:
  def deposit_money(self):
    amount=float(input("Enter Deposit Amount:Rs."))

    if (amount>0):
      self.accounts[self.current_user]["Balance"]+=amount
      print(f"\nRs.{amount:.2f} Deposited Successfully.\n {self.add_timestamp()}")
      print(f"\nUpdated Balance:Rs.{self.accounts[self.current_user]["Balance"]:.2f}")
      self.accounts[self.current_user]["Mini-Statement"].append(
          f"Deposited->Rs.{amount:.2f}  {self.add_timestamp()}"
      )
      self.save_data()
    else:
      print("\nInvalid Amount.")


# Withdraw Money:
  def withdraw_money(self):
    amount=float(input("Enter Withdraw Amount:Rs."))
    current_bal = self.accounts[self.current_user]["Balance"]
    if (amount<=0):
      print(f"\nInvalid Amount.")
    elif (amount>current_bal):
      print(f"\nInsufficient Balance.")
    else:
      current_bal-=amount
      print(f"\nRs.{amount:.2f} Withdrawal Successful.\n {self.add_timestamp()}")
      print(f"Remaining Balance:Rs.{current_bal:.2f}")

      self.accounts[self.current_user]["Mini-Statement"].append(
          f"Withdrawn->Rs.{amount:.2f}  {self.add_timestamp()}"
      )
      self.save_data()


# Change Pin:
  def change_pin(self):
    old_pin=input("Enter Old PIN:")

    if (old_pin==self.accounts[self.current_user]["PIN"]):
      new_pin=input("Enter New PIN:")
      confirm=input("Confirm New PIN:")

      if (new_pin==confirm):
        self.accounts[self.current_user]["PIN"]=new_pin
        print(f"\nPIN Changed Successfully.\n {self.add_timestamp()}")
        self.accounts[self.current_user]["Mini-Statement"].append(
          f"PIN Changed on {self.add_timestamp()}"
        )
        self.save_data()
      else:
        print("\nPIN Mismatch!")
    else:
      print("\nWrong Old PIN!")

# Mini Statement:
  def show_miniStatement(self):
    print("\n=====Mini Statement=====")
    if (len(self.accounts[self.current_user]["Mini-Statement"])==0):
      print("\nNo Transactions Yet.")
    else:
      for item in self.accounts[self.current_user]["Mini-Statement"]:
        print("*",item)
    print("=========================")

# Exiting and Saving data 
  def exit(self):
    self.accounts[self.current_user]["Mini-Statement"].append(f"\nLogged out Successfully.  {self.add_timestamp()}")
    self.save_data()
    print("\nLogged out Successfully.\nThank You for using ATM.")
    exit()

# ATM Menu:
  def atm_menu(self):
    while True:
      print("\n=====ATM MENU=====")
      print("1.Check Balance")
      print("2.Deposit Money")
      print("3.Withdraw Money")
      print("4.Change Pin")
      print("5.Mini Statement")
      print("6.Exit")
      print("====================")

      choice=input("Enter Your Choice:")

      if (choice=="1"):
        self.check_balance()
      elif (choice=="2"):
        self.deposit_money()
      elif (choice=="3"):
        self.withdraw_money()
      elif (choice=="4"):
        self.change_pin()
      elif (choice=="5"):
        self.show_miniStatement()
      elif(choice=="6"):
        self.exit()
        break
      else:
        print("\nInvalid Choice!")

# Main Program:
if __name__ == "__main__":
    atm = ATM()
    
    while True:
        print("\n===== WELCOME TO THE ATM =====")
        print("1. Login to Existing Account")
        print("2. Open a New Account")
        print("3. Exit System")
        print("==============================")
        
        start_choice = input("Select an option: ")
        
        if start_choice == "1":
            # Only go to the ATM menu if login is successful
            if atm.authenticate():
                atm.atm_menu() 
        elif start_choice == "2":
            atm.create_account()
        elif start_choice == "3":
            print("\nThank you for visiting. Goodbye!")
            break
        else:
            print("\nInvalid selection! Please enter 1, 2, or 3.")