#FINAL PROJECT:ATM SYSTEM.
import datetime


class ATM:
  def __init__(self):
    self.pin="12345"
    self.balance=5000
    self.mini_statement=[]

# Adding Timestamps with actions:
  def add_timestamp(self):
    presenthour=datetime.datetime.now().strftime("%d/%m/%Y  %H:%M:%S")
    return presenthour


# Authentication:
  def authenticate(self):
    attempts=3

    while attempts>0:
      entered_pin=input("Enter You Pin:")

      if (entered_pin==self.pin):
        print("\nLogin Successful.")
        return True
      else:
        attempts-=1
        print(f"Incorrect Pin.\nAttempts Left:{attempts}")

    print("\nToo many wrong Attempts.")
    return False

# Check Balance:
  def check_balance(self):
    print(f"\nCurrent Balance:Rs.{self.balance:.2f}\n{self.add_timestamp()}")
    self.mini_statement.append(
        f"Check Balance -> Rs.{self.balance:.2f}   {self.add_timestamp()}"
    )

# Deposit Money:
  def deposit_money(self):
    amount=float(input("Enter Deposit Amount:Rs."))

    if (amount>0):
      self.balance+=amount
      print(f"\nRs.{amount:.2f} Deposited Successfully.\n {self.add_timestamp()}")
      print(f"\nUpdated Balance:Rs.{self.balance:.2f}")
      self.mini_statement.append(
          f"Deposited->Rs.{amount:.2f}  {self.add_timestamp()}"
      )
    else:
      print("\nInvalid Amount.")

# Withdraw Money:
  def withdraw_money(self):
    amount=float(input("Enter Withdraw Amount:Rs."))

    if (amount<=0):
      print("\nInvalid Amount.")
    elif (amount>self.balance):
      print("\nInsufficient Balance.")
    else:
      self.balance-=amount
      print(f"\nRs.{amount:.2f} Withdrawal Successful.\n {self.add_timestamp()}")
      print(f"Remaining Balance:Rs.{self.balance:.2f}")

      self.mini_statement.append(
          f"Withdrawn->Rs.{amount:.2f}  {self.add_timestamp()}"
      )
# Change Pin:
  def change_pin(self):
    old_pin=input("Enter Old PIN:")

    if (old_pin==self.pin):
      new_pin=input("Enter New PIN:")
      confirm=input("Confirm New PIN:")

      if (new_pin==confirm):
        self.pin=new_pin
        print("\nPIN Changed Successfully.\n {self.add_timestamp()}")
        self.mini_statement.append(
          f"PIN Changed on {self.add_timestamp()}"
        )
      else:
        print("\nPIN Mismatch!")
    else:
      print("\nWrong Old PIN!")

# Mini Statement:
  def show_miniStatement(self):
    print("\n=====Mini Statement=====")
    if (len(self.mini_statement)==0):
      print("\nNo Transactions Yet.")
    else:
      for item in self.mini_statement:
        print("*",item)
    print("=========================")



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
        print("\nThank You for using ATM")
        break
      else:
        print("\nInvalid Choice!")

# Main Program:
atm=ATM()

if (atm.authenticate()):
  atm.atm_menu()