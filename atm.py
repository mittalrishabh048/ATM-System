# ATM SYSTEM.
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

# Generating Transaction ID
  def transaction_id(self):
    id_num=str(random.randint(100000,999999))
    txn_id="TXN"+id_num
    return txn_id

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
      transaction__id=self.transaction_id()
      self.accounts[self.current_user]["Balance"]+=amount
      print(f"\nTransaction ID:{transaction__id} | Rs.{amount:.2f} Deposited Successfully.\n {self.add_timestamp()}")
      print(f"\nUpdated Balance:Rs.{self.accounts[self.current_user]["Balance"]:.2f}")
      self.accounts[self.current_user]["Mini-Statement"].append(
          f"Transaction ID:{transaction__id} | Deposited->Rs.{amount:.2f}  {self.add_timestamp()}"
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
      transaction__id=self.transaction_id()
      self.accounts[self.current_user]["Balance"]-=amount
      updated_bal=self.accounts[self.current_user]["Balance"]
      print(f"\nTransaction ID:{transaction__id} | Rs.{amount:.2f} Withdrawal Successful.\n {self.add_timestamp()}")
      print(f"Remaining Balance:Rs.{updated_bal:.2f}")

      self.accounts[self.current_user]["Mini-Statement"].append(
          f"Transaction ID:{transaction__id} | Withdrawn->Rs.{amount:.2f}  {self.add_timestamp()}"
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

# Transfer Money
  def transfer_money(self):
    # Step_1:Taking input of Receiver's Account Number and Amount To Transfer
    receiver_acc_num=input("Enter The Receiver's Account Number:")
    

    # Step_2:Validating the Data
    # A:Receiver Account existence
    if receiver_acc_num not in self.accounts:
      print("Account Not Found!")
      return
    
    # B: Self Transfer Prevention
    if receiver_acc_num==self.current_user:
      print("\nCan't Transfer to your own Account")
      return
    
    # Step 3: Safely taking input of Amount to Transfer
    amount_to_transfer = float(input("Enter The Amount To Transfer: "))
    
    
    # C:Amount Validity
    if (amount_to_transfer<=0):
      print("\nInvalid Amount!")
      return
    # D:Sufficent Balance
    if (amount_to_transfer>self.accounts[self.current_user]["Balance"]):
      print("\nInsufficient Balance")
      return
    
    # If the code reaches this point, all validation checks have passed!
    print("\nValidation Successful. Processing transaction...")

  # Step_3:Maths and Logs
    transaction__id=self.transaction_id()
    self.accounts[self.current_user]["Balance"]-=amount_to_transfer
    self.accounts[receiver_acc_num]["Balance"]+=amount_to_transfer

    # Append to both mini-statements
    self.accounts[self.current_user]["Mini-Statement"].append(
      f"Transaction ID:{transaction__id} | Transferred -> Rs.{amount_to_transfer:.2f} to Acc:{receiver_acc_num}   {self.add_timestamp()}"
      )
    self.accounts[receiver_acc_num]["Mini-Statement"].append(
      f"Transaction ID:{transaction__id} | Received -> Rs.{amount_to_transfer:.2f} from Acc:{self.current_user}   {self.add_timestamp()}"
      )
    
    # Save to file and notify user
    self.save_data()
    print(f"\nTransaction Successful! Remaining Balance: Rs.{self.accounts[self.current_user]['Balance']:.2f}")



# Mini Statement:
  def show_miniStatement(self):
    print("\n=====Mini Statement=====")
    if (len(self.accounts[self.current_user]["Mini-Statement"])==0):
      print("\nNo Transactions Yet.")
    else:
      for item in self.accounts[self.current_user]["Mini-Statement"]:
        print("*",item)
    print("=========================")

# Logging out
  def logout(self):
    self.accounts[self.current_user]["Mini-Statement"].append(
      f"Logged out Successfully.   {self.add_timestamp()}"
    )
    self.save_data()
    print("\nLogged out Successfully.")
    print("\nThank You for using ATM.")

    # Clear the session state variable
    self.current_user=None

# Exiting and Saving data 
  def exit(self):
    self.accounts[self.current_user]["Mini-Statement"].append(f"\nLogged out Successfully.  {self.add_timestamp()}")
    self.save_data()
    print("\nExited Successfully.\nThank You for using ATM.")
    exit()

# ATM Menu:
  def atm_menu(self):
    while True:
      print("\n=====ATM MENU=====")
      print("1.Check Balance")
      print("2.Deposit Money")
      print("3.Withdraw Money")
      print("4.Transfer Money")
      print("5.Change Pin")
      print("6.Mini Statement")
      print("7.Logout (Return to Welcome Menu)")
      print("8.Exit(Close System Completely)")
      print("====================")

      choice=input("Enter Your Choice:")

      if (choice=="1"):
        self.check_balance()
      elif (choice=="2"):
        self.deposit_money()
      elif (choice=="3"):
        self.withdraw_money()
      elif (choice=="4"):
        self.transfer_money()
      elif (choice=="5"):
        self.change_pin()
      elif (choice=="6"):
        self.show_miniStatement()
      elif(choice=="7"):
        self.logout()
        break
      elif(choice=="8"):
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
        print("2. Create a New Account")
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
            print("\nSystem Shutting Down. Goodbye!")
            break
        else:
            print("\nInvalid selection! Please enter 1, 2, or 3.")