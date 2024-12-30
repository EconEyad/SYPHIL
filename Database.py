import psycopg2
from urllib.parse import urlparse
import streamlit as st

# Function to connect to PostgreSQL
def get_postgres_connection():
    DATABASE_URL = st.secrets["DATABASE_URL"]
    parsed_url = urlparse(DATABASE_URL)
    return psycopg2.connect(
        dbname=parsed_url.path[1:],  # Removes the leading '/'
        user=parsed_url.username,
        password=parsed_url.password,
        host=parsed_url.hostname,
        port=parsed_url.port
    )

def initialize_database(conn):
    with conn.cursor() as c:
        # 1: Create Buyer table
        c.execute("""
        CREATE TABLE IF NOT EXISTS Buyer (
            ID SERIAL UNIQUE NOT NULL PRIMARY KEY,
            Name TEXT NOT NULL UNIQUE,
            Address TEXT NOT NULL UNIQUE,
            Contract_details INT NOT NULL UNIQUE
        );
        """)

        # 2: Create Printer table
        c.execute("""
        CREATE TABLE IF NOT EXISTS Printer (
            ID SERIAL UNIQUE NOT NULL PRIMARY KEY,
            Name TEXT NOT NULL UNIQUE,
            Address TEXT NOT NULL UNIQUE,
            Contract_details INT NOT NULL UNIQUE
        );
        """)

        # 3: Create Product table
        c.execute("""
        CREATE TABLE IF NOT EXISTS Product (
            ID SERIAL UNIQUE NOT NULL PRIMARY KEY,
            Item_desc TEXT NOT NULL UNIQUE
        )
        """)
        # 4: Create Supplier table
        c.execute("""
        CREATE TABLE IF NOT EXISTS Supplier (
            ID SERIAL UNIQUE NOT NULL PRIMARY KEY,
            Name TEXT NOT NULL UNIQUE,
            Address TEXT NOT NULL UNIQUE,
            Contract_details INT NOT NULL UNIQUE
        )
        """)

        # 5: Create Agent table
        c.execute("""
        CREATE TABLE IF NOT EXISTS Agent (
            ID SERIAL UNIQUE NOT NULL PRIMARY KEY,
            Name TEXT NOT NULL UNIQUE,
            Address TEXT NOT NULL UNIQUE,
            Contract_details INT NOT NULL UNIQUE
        )
        """)

        # 6: Create Invoice table
        c.execute("""
        CREATE TABLE IF NOT EXISTS Invoice (
            ID SERIAL UNIQUE NOT NULL PRIMARY KEY,
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
        CREATE TABLE IF NOT EXISTS Date (
            ID SERIAL UNIQUE NOT NULL PRIMARY KEY,
            Year INT NOT NULL,
            Quarter INT NOT NULL,
            Month INT NOT NULL,
            Day INT NOT NULL
        )
        """)
        # 8: Create Revenue table
        c.execute("""
        CREATE TABLE IF NOT EXISTS Revenue (
            ID SERIAL UNIQUE NOT NULL PRIMARY KEY,
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

# Initialize the database
conn = get_postgres_connection()
initialize_database(conn)
conn.close()