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
      "Transactions":[f"Account Created on {self.add_timestamp()}"]
    }
    self.save_data()
    print(f"Account Created Successfully.\nYour Account Number is:{new_acc_num}.\nPlease remember this number to login.")
                      
# Check Balance:
  def check_balance(self):
    current_bal=self.accounts[self.current_user]["Balance"]
    print(f"\nCurrent Balance:Rs.{current_bal:.2f}\n{self.add_timestamp()}")
    self.accounts[self.current_user]["Transactions"].append(
        f"Check Balance -> Rs.{current_bal:.2f}   {self.add_timestamp()}"
    )

# Better Input Validation 
  def get_valid_input(self,prompt):
    while True:
      try:
        user_input=input(prompt).strip()
        amount=float(user_input)

        if amount<=0:
          print("\nAmount must be greater than zero. Please try again.")
          continue
        return amount
      
      except ValueError:
        print("\nInvalid input! Please enter a valid number without letters or symbols.")


# Deposit Money:
  def deposit_money(self):
    amount=self.get_valid_input("Enter Deposit Amount:Rs.")

    transaction__id=self.transaction_id()
    self.accounts[self.current_user]["Balance"]+=amount
    print(f"\nTransaction ID:{transaction__id} | Rs.{amount:.2f} Deposited Successfully.\n {self.add_timestamp()}")
    print(f"\nUpdated Balance:Rs.{self.accounts[self.current_user]["Balance"]:.2f}")
    self.accounts[self.current_user]["Transactions"].append(
        f"Transaction ID:{transaction__id} | Deposited->Rs.{amount:.2f}  {self.add_timestamp()}"
      )
    self.save_data()


# Withdraw Money:
  def withdraw_money(self):
    amount=self.get_valid_input("Enter Withdraw Amount:Rs.")
    current_bal = self.accounts[self.current_user]["Balance"]
    
    if (amount>current_bal):
      print(f"\nInsufficient Balance.")
      return

    transaction__id=self.transaction_id()
    self.accounts[self.current_user]["Balance"]-=amount
    updated_bal=self.accounts[self.current_user]["Balance"]
    print(f"\nTransaction ID:{transaction__id} | Rs.{amount:.2f} Withdrawal Successful.\n {self.add_timestamp()}")
    print(f"Remaining Balance:Rs.{updated_bal:.2f}")

    self.accounts[self.current_user]["Transactions"].append(
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
        self.accounts[self.current_user]["Transactions"].append(
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
    amount_to_transfer = self.get_valid_input("Enter The Amount To Transfer: ")
    
    
    
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

    # Append to both Transactionss
    self.accounts[self.current_user]["Transactions"].append(
      f"Transaction ID:{transaction__id} | Transferred -> Rs.{amount_to_transfer:.2f} to Acc:{receiver_acc_num}   {self.add_timestamp()}"
      )
    self.accounts[receiver_acc_num]["Transactions"].append(
      f"Transaction ID:{transaction__id} | Received -> Rs.{amount_to_transfer:.2f} from Acc:{self.current_user}   {self.add_timestamp()}"
      )
    
    # Save to file and notify user
    self.save_data()
    print(f"\nTransaction Successful! Remaining Balance: Rs.{self.accounts[self.current_user]['Balance']:.2f}")



# Transactions:
  def transactions(self):
    print("\n=====Transactions History (Newest Above) =====")
    history = self.accounts[self.current_user]["Transactions"]

    if not history:
      print("No Transactions Yet.")
      print("===============================")
      return
    
    # Start by showing the most recent 5 items
    count = 5
    recent_history = history[-count:]
        
    for item in reversed(recent_history):
      print("*", item)
    print("===============================")

    while count < len(history):
      remaining = len(history) - count
      print(f"\n[ ↓ {remaining} older transaction(s) hidden ]")
      choice = input("Press [Enter] to load more, or [q] to exit: ").strip().lower()

      if choice=='q':
        break

      # Expand the view by pulling the next batch of 5 records
      count += 5
      recent_history = history[-count:]
            
      print("\n===== Expanded History =====")
      for item in reversed(recent_history):
        print("*", item)
      print("============================")

# Logging out
  def logout(self):
    self.accounts[self.current_user]["Transactions"].append(
      f"Logged out Successfully.   {self.add_timestamp()}"
    )
    self.save_data()
    print("\nLogged out Successfully.")
    print("\nThank You for using ATM.")

    # Clear the session state variable
    self.current_user=None

# Exiting and Saving data 
  def exit(self):
    self.accounts[self.current_user]["Transactions"].append(f"\nLogged out Successfully.  {self.add_timestamp()}")
    self.save_data()
    print("\nExited Successfully.\nThank You for using ATM.")
    exit()

# Account Deletion
  def del_acc(self):
    print("\n===== !!! WARNING !!! =====")
    print("Account deletion is permanent. All your data and balance will be lost forever.")

    confirm_pin = input("Enter your 4-Digit PIN to verify ownership: ").strip()
    stored_pin = self.accounts[self.current_user]["PIN"]

    if(confirm_pin!=stored_pin):
      print("\nIncorrect PIN! Deletion cancelled for security.")
      return
    
    final_check = input("\nAre you absolutely sure you want to delete your account? (yes/no): ").strip().lower()

    if final_check in ['yes', 'y']:
      acc_to_delete = self.current_user
        
      del self.accounts[acc_to_delete]
      self.save_data()
        
      self.current_user = None
      print(f"\nAccount {acc_to_delete} has been successfully deleted from the system.")
      print("Returning to the main welcome screen.")
    else:
      print("\nDeletion cancelled. Your account remains active.")


# ATM Menu:
  def atm_menu(self):
    while True:
      print("\n=====ATM MENU=====")
      print("1.Check Balance")
      print("2.Deposit Money")
      print("3.Withdraw Money")
      print("4.Transfer Money")
      print("5.Change Pin")
      print("6.Transactions History")
      print("7.Logout (Return to Welcome Menu)")
      print("8.Exit(Close System Completely)")
      print("9.Delete Account")
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
        self.transactions()
      elif(choice=="7"):
        self.logout()
        break
      elif(choice=="8"):
        self.exit()
        break
      elif(choice=="9"):
        self.del_acc()
        break # Breaks the menu loop since the account session is gone
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