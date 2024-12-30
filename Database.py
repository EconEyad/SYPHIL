import numpy as np
import pandas as pd
import sqlite3
conn = sqlite3.connect('Transaction.sqlite3')
conn.execute("PRAGMA foreign_keys = ON;")  # Enable foreign key enforcement
c = conn.cursor()

# 1: Create Product table
c.execute("""
CREATE TABLE Product (
    ID INTEGER UNIQUE NOT NULL PRIMARY KEY AUTOINCREMENT,
    Item_desc TEXT NOT NULL UNIQUE
)
""")

# 2: Create Printer table
c.execute("""
CREATE TABLE Printer (
    ID INTEGER UNIQUE NOT NULL PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL UNIQUE,
    Address TEXT NOT NULL UNIQUE,
    Contract_details INT NOT NULL UNIQUE 
)
""")

# 3: Create Buyer table
c.execute("""
CREATE TABLE Buyer (
    ID INTEGER UNIQUE NOT NULL PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL UNIQUE,
    Address TEXT NOT NULL UNIQUE,
    Contract_details INT NOT NULL UNIQUE
)
""")

# 4: Create Supplier table
c.execute("""
CREATE TABLE Supplier (
    ID INTEGER UNIQUE NOT NULL PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL UNIQUE,
    Address TEXT NOT NULL UNIQUE,
    Contract_details INT NOT NULL UNIQUE
)
""")

# 5: Create Agent table
c.execute("""
CREATE TABLE Agent (
    ID INTEGER UNIQUE NOT NULL PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL UNIQUE,
    Address TEXT NOT NULL UNIQUE,
    Contract_details INT NOT NULL UNIQUE
)
""")

# 6: Create Invoice table
c.execute("""
CREATE TABLE Invoice (
    ID INTEGER UNIQUE NOT NULL PRIMARY KEY AUTOINCREMENT,
    Payment_request_num TEXT NOT NULL,
    Delivery_client_num TEXT NOT NULL,
    Billing_num TEXT NOT NULL,
    Collection_num TEXT NOT NULL,
    Deposit_cheque_num TEXT NOT NULL,
    Status TEXT NOT NULL CHECK(Status IN ('Approved', 'Disapproved'))
)
""")

# 7: Create Date table
c.execute("""
CREATE TABLE Date (
    ID INTEGER UNIQUE NOT NULL PRIMARY KEY AUTOINCREMENT,
    Year INT NOT NULL,
    Quarter INT NOT NULL ,
    Month INT NOT NULL,
    Day INT NOT NULL 
)
""")

# 8: Create Revenue table
c.execute("""
CREATE TABLE Revenue (
    ID INTEGER UNIQUE NOT NULL PRIMARY KEY AUTOINCREMENT,
    ID_buyer INT NOT NULL REFERENCES Buyer(ID),
    ID_printer INT NOT NULL REFERENCES Printer(ID),
    ID_product INT NOT NULL REFERENCES Product(ID),
    ID_agent INT NOT NULL REFERENCES Agent(ID),
    ID_supplier INT NOT NULL REFERENCES Supplier(ID),
    ID_invoice INT NOT NULL REFERENCES Invoice(ID),
    ID_date INT NOT NULL REFERENCES Date(ID),
    Price_per_item REAL NOT NULL,
    Cost_per_item REAL NOT NULL,
    Print_per_item REAL NOT NULL,
    Commission_rate REAL NOT NULL,
    Production_start_date INT NOT NULL,
    Delivery_date INT NOT NULL,
    Billing_date INT NOT NULL,
    Payment_date INT NOT NULL
)
""")

conn.commit()
conn.close()

# Streamlit:

# Connect to the database
conn = sqlite3.connect('Transaction.sqlite3')
conn.execute("PRAGMA foreign_keys = ON;")  # Ensure foreign key constraints
c = conn.cursor()
