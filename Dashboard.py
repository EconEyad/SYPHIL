import streamlit as st
import psycopg2
from urllib.parse import urlparse

# Connect to the SQLite database
DATABASE_URL = st.secrets["DATABASE_URL"]

def get_postgres_connection():
    DATABASE_URL = st.secrets["DATABASE_URL"]
    parsed_url = urlparse(DATABASE_URL)
    
    try:
        connection = psycopg2.connect(
            dbname=parsed_url.path[1:],  # Removes the leading "/"
            user=parsed_url.username,
            password=parsed_url.password,
            host=parsed_url.hostname,
            port=parsed_url.port
        )
        return connection
    except Exception as e:
        st.error(f"Failed to connect to database: {e}")
        raise e

# Connect to the PostgreSQL database
conn = get_postgres_connection()
c = conn.cursor()

import streamlit as st
import psycopg2
from urllib.parse import urlparse

# Use DATABASE_URL from Streamlit secrets
DATABASE_URL = st.secrets["DATABASE_URL"]

# Function to connect to PostgreSQL
def get_postgres_connection():
    parsed_url = urlparse(DATABASE_URL)
    return psycopg2.connect(
        dbname=parsed_url.path[1:],  # Removes the leading "/"
        user=parsed_url.username,
        password=parsed_url.password,
        host=parsed_url.hostname,
        port=parsed_url.port
    )

# Connect to the PostgreSQL database
conn = get_postgres_connection()
c = conn.cursor()

st.title("Transaction Entry Dashboard")

# Form to input transaction details
with st.form("transaction_form"):
    # Buyer Details
    buyer_name = st.text_input("Buyer Name")
    buyer_address = st.text_input("Buyer Address")
    buyer_contract = st.number_input("Buyer Contract Details", step=1, min_value=0)

    # Printer Details
    printer_name = st.text_input("Printer Name")
    printer_address = st.text_input("Printer Address")
    printer_contract = st.number_input("Printer Contract Details", step=1, min_value=0)

    # Product Details
    product_desc = st.text_input("Product Description")

    # Supplier Details
    supplier_name = st.text_input("Supplier Name")
    supplier_address = st.text_input("Supplier Address")
    supplier_contract = st.number_input("Supplier Contract Details", step=1, min_value=0)

    # Agent Details
    agent_name = st.text_input("Agent Name")
    agent_address = st.text_input("Agent Address")
    agent_contract = st.number_input("Agent Contract Details", step=1, min_value=0)

    # Invoice Details
    payment_request_num = st.text_input("Payment Request Invoice Number")
    delivery_client_num = st.text_input("Delivery Client Invoice Number")
    billing_num = st.text_input("Billing Invoice Number")
    collection_num = st.text_input("Collection Invoice Number")
    deposit_cheque_num = st.text_input("Deposit Cheque Invoice Number")
    invoice_status = st.selectbox("Invoice Status", ["Approved", "Disapproved"])

    # Date Details
    year = st.number_input("Year", step=1, min_value=2000, max_value=2100)
    quarter = st.number_input("Quarter", step=1, min_value=1, max_value=4)
    month = st.number_input("Month", step=1, min_value=1, max_value=12)
    day = st.number_input("Day", step=1, min_value=1, max_value=31)

    # Revenue Details
    price_per_item = st.number_input("Price Per Item", step=0.01, min_value=0.0)
    cost_per_item = st.number_input("Cost Per Item", step=0.01, min_value=0.0)
    print_per_item = st.number_input("Print Per Item", step=0.01, min_value=0.0)
    commission_rate = st.number_input("Commission Rate", step=0.01, min_value=0.0)
    production_start_date = st.number_input("Production Start Date (YYYYMMDD)", step=1, min_value=20000000, max_value=21000000)
    delivery_date = st.number_input("Delivery Date (YYYYMMDD)", step=1, min_value=20000000, max_value=21000000)
    billing_date = st.number_input("Billing Date (YYYYMMDD)", step=1, min_value=20000000, max_value=21000000)
    payment_date = st.number_input("Payment Date (YYYYMMDD)", step=1, min_value=20000000, max_value=21000000)

    submitted = st.form_submit_button("Submit Transaction")

    if submitted:
        try:
            # Insert or get ID for Buyer
            c.execute("""
                INSERT INTO Buyer (Name, Address, Contract_details)
                VALUES (%s, %s, %s) ON CONFLICT (Name, Address) DO NOTHING
            """, (buyer_name, buyer_address, buyer_contract))
            conn.commit()
            c.execute("SELECT ID FROM Buyer WHERE Name = %s AND Address = %s", (buyer_name, buyer_address))
            buyer_id = c.fetchone()[0]

            # Insert or get ID for Printer
            c.execute("""
                INSERT INTO Printer (Name, Address, Contract_details)
                VALUES (%s, %s, %s) ON CONFLICT (Name, Address) DO NOTHING
            """, (printer_name, printer_address, printer_contract))
            conn.commit()
            c.execute("SELECT ID FROM Printer WHERE Name = %s AND Address = %s", (printer_name, printer_address))
            printer_id = c.fetchone()[0]

            # Insert or get ID for Product
            c.execute("""
                INSERT INTO Product (Item_desc)
                VALUES (%s) ON CONFLICT (Item_desc) DO NOTHING
            """, (product_desc,))
            conn.commit()
            c.execute("SELECT ID FROM Product WHERE Item_desc = %s", (product_desc,))
            product_id = c.fetchone()[0]

            # Insert or get ID for Supplier
            c.execute("""
                INSERT INTO Supplier (Name, Address, Contract_details)
                VALUES (%s, %s, %s) ON CONFLICT (Name, Address) DO NOTHING
            """, (supplier_name, supplier_address, supplier_contract))
            conn.commit()
            c.execute("SELECT ID FROM Supplier WHERE Name = %s AND Address = %s", (supplier_name, supplier_address))
            supplier_id = c.fetchone()[0]

            # Insert or get ID for Agent
            c.execute("""
                INSERT INTO Agent (Name, Address, Contract_details)
                VALUES (%s, %s, %s) ON CONFLICT (Name, Address) DO NOTHING
            """, (agent_name, agent_address, agent_contract))
            conn.commit()
            c.execute("SELECT ID FROM Agent WHERE Name = %s AND Address = %s", (agent_name, agent_address))
            agent_id = c.fetchone()[0]

            # Insert Invoice
            c.execute("""
                INSERT INTO Invoice (Payment_request_num, Delivery_client_num, Billing_num, Collection_num, Deposit_cheque_num, Status)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING ID
            """, (payment_request_num, delivery_client_num, billing_num, collection_num, deposit_cheque_num, invoice_status))
            conn.commit()
            invoice_id = c.fetchone()[0]

            # Insert Date
            c.execute("""
                INSERT INTO Date (Year, Quarter, Month, Day)
                VALUES (%s, %s, %s, %s)
            """, (year, quarter, month, day))
            conn.commit()
            c.execute("SELECT ID FROM Date WHERE Year = %s AND Quarter = %s AND Month = %s AND Day = %s",
                      (year, quarter, month, day))
            date_id = c.fetchone()[0]

            # Insert into Revenue
            c.execute("""
                INSERT INTO Revenue (ID_buyer, ID_printer, ID_product, ID_agent, ID_supplier, ID_invoice, ID_date,
                                     Price_per_item, Cost_per_item, Print_per_item, Commission_rate,
                                     Production_start_date, Delivery_date, Billing_date, Payment_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (buyer_id, printer_id, product_id, agent_id, supplier_id, invoice_id, date_id,
                  price_per_item, cost_per_item, print_per_item, commission_rate,
                  production_start_date, delivery_date, billing_date, payment_date))
            conn.commit()

            st.success("Transaction submitted successfully!")

        except Exception as e:
            conn.rollback()  # Roll back transaction on error
            st.error(f"An error occurred: {e}")