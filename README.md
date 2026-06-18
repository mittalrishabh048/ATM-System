# 🏦 Robust ATM Banking System (Python + JSON)

A command-line ATM banking system built with Python. What started as a simple single-user ATM project gradually evolved into a multi-user banking engine with persistent storage, transaction tracking, account management, validation systems, and daily transaction limits.

This project was created as part of my Python learning journey after completing the Apna College Python course. The main goal was not only to build features but also to understand how software grows through iterative improvements, testing, debugging, and refactoring.

---

## 📌 Project Overview

This ATM system allows multiple users to create accounts, securely log in, manage balances, transfer money, track transactions, and persist all data using JSON files.

The project simulates many real-world banking concepts such as:

* User authentication
* Account creation
* Session management
* Deposits and withdrawals
* Money transfers between accounts
* Transaction history
* Daily transaction limits
* Persistent data storage
* Account deletion workflows

---

## 🚀 Features

### 👤 Account Management

* Create new accounts
* Automatically generated account numbers
* Secure 4-digit PIN system
* Multi-user support
* Account deletion with verification

### 🔐 Authentication

* Login using account number and PIN
* 3-attempt PIN verification system
* Session tracking using `current_user`

### 💰 Banking Operations

* Check balance
* Deposit money
* Withdraw money
* Transfer money between accounts

### 📜 Transaction System

* Unique transaction IDs (`TXN######`)
* Transaction history tracking
* Last 5 transactions displayed first
* Load older transactions on demand
* Transaction logs for both sender and receiver during transfers

### 🛡️ Validation & Security

* Input validation using `try-except`
* Protection against invalid account transfers
* Prevention of self-transfers
* Insufficient balance checks
* PIN verification before account deletion

### 📊 Daily Limits

The system automatically tracks and enforces daily limits:

| Operation  | Daily Limit |
| ---------- | ----------- |
| Deposit    | ₹50,000     |
| Withdrawal | ₹25,000     |
| Transfer   | ₹30,000     |

Daily counters automatically reset when the calendar date changes.

### 💾 Persistent Storage

* Uses JSON as a lightweight database
* Stores account information permanently
* Automatically saves updates
* Reloads account data on startup

---

## 🏗️ Technologies Used

* Python
* Object-Oriented Programming (OOP)
* JSON File Handling
* Dictionaries & Nested Data Structures
* Exception Handling
* Git & GitHub

---

## 📂 Project Structure

```text
ATM-System/
│
├── atm.py
├── accounts_data.json
└── README.md
```

---

## 🧠 What I Learned

While building and improving this project, I learned:

* How to design and manage multi-user systems
* How to store and retrieve data using JSON
* How session management works using a `current_user`
* How to work with nested dictionaries
* How to validate user input safely
* How to implement business rules such as daily limits
* How to break large features into smaller problems
* How to debug logical errors through testing
* How to use Git and GitHub for version control
* How software projects evolve through continuous improvements

---

## 🤖 AI Usage Disclosure

I want to be transparent about how this project was built.

This project was not written entirely from scratch by me. I actively used AI tools to help generate code, explore implementation approaches, and learn new concepts.

However, I was responsible for:

* Choosing the project features
* Making architectural and design decisions
* Testing and debugging the application
* Understanding and modifying the generated code
* Deciding how each feature should work
* Iteratively improving the project over multiple versions

I view this project as a learning experience where AI acted as a mentor and coding assistant rather than a replacement for understanding.

---

## 🔮 Possible Future Improvements

* Fast Cash feature
* Interest calculation system
* Admin dashboard
* Password encryption/hashing
* Database integration (SQLite/MySQL)
* Separate Account and Transaction classes
* GUI version using Tkinter or PyQt
* Export transaction history to CSV/PDF

---

## 📈 Project Evolution

Version 1:

* Single-user ATM
* Hardcoded balance and PIN

Version 2:

* JSON-based persistent storage
* Transaction history
* Timestamps

Version 3:

* Multi-user account system
* Account creation
* Transfers
* Daily limits
* Account deletion
* Improved validation

---

## 🙌 Final Note

This project represents an important milestone in my programming journey. More than the final features, it taught me how to think about software design, data management, validation, debugging, and iterative development.

I plan to continue improving my Python skills by building more projects and eventually moving toward AI and Machine Learning.