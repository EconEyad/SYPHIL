import streamlit as st
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('Transaction.sqlite3')
conn.execute("PRAGMA foreign_keys = ON;")  # Enable foreign key constraints
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
            c.execute("INSERT OR IGNORE INTO Buyer (Name, Address, Contract_details) VALUES (?, ?, ?)", 
                      (buyer_name, buyer_address, buyer_contract))
            buyer_id = c.execute("SELECT ID FROM Buyer WHERE Name = ? AND Address = ?", (buyer_name, buyer_address)).fetchone()[0]

            # Insert or get ID for Printer
            c.execute("INSERT OR IGNORE INTO Printer (Name, Address, Contract_details) VALUES (?, ?, ?)", 
                      (printer_name, printer_address, printer_contract))
            printer_id = c.execute("SELECT ID FROM Printer WHERE Name = ? AND Address = ?", (printer_name, printer_address)).fetchone()[0]

            # Insert or get ID for Product
            c.execute("INSERT OR IGNORE INTO Product (Item_desc) VALUES (?)", (product_desc,))
            product_id = c.execute("SELECT ID FROM Product WHERE Item_desc = ?", (product_desc,)).fetchone()[0]

            # Insert or get ID for Supplier
            c.execute("INSERT OR IGNORE INTO Supplier (Name, Address, Contract_details) VALUES (?, ?, ?)", 
                      (supplier_name, supplier_address, supplier_contract))
            supplier_id = c.execute("SELECT ID FROM Supplier WHERE Name = ? AND Address = ?", (supplier_name, supplier_address)).fetchone()[0]

            # Insert or get ID for Agent
            c.execute("INSERT OR IGNORE INTO Agent (Name, Address, Contract_details) VALUES (?, ?, ?)", 
                      (agent_name, agent_address, agent_contract))
            agent_id = c.execute("SELECT ID FROM Agent WHERE Name = ? AND Address = ?", (agent_name, agent_address)).fetchone()[0]

            # Insert or get ID for Invoice
            c.execute("INSERT INTO Invoice (Payment_request_num, Delivery_client_num, Billing_num, Collection_num, Deposit_cheque_num, Status) VALUES (?, ?, ?, ?, ?, ?)", 
                      (payment_request_num, delivery_client_num, billing_num, collection_num, deposit_cheque_num, invoice_status))
            invoice_id = c.lastrowid

            # Insert or get ID for Date
            c.execute("INSERT OR IGNORE INTO Date (Year, Quarter, Month, Day) VALUES (?, ?, ?, ?)", 
                      (year, quarter, month, day))
            date_id = c.execute("SELECT ID FROM Date WHERE Year = ? AND Quarter = ? AND Month = ? AND Day = ?", 
                                (year, quarter, month, day)).fetchone()[0]

            # Insert into Revenue
            c.execute("""INSERT INTO Revenue (ID_buyer, ID_printer, ID_product, ID_agent, ID_supplier, ID_invoice, ID_date, 
                        Price_per_item, Cost_per_item, Print_per_item, Commission_rate, Production_start_date, Delivery_date, Billing_date, Payment_date) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                      (buyer_id, printer_id, product_id, agent_id, supplier_id, invoice_id, date_id, price_per_item, 
                       cost_per_item, print_per_item, commission_rate, production_start_date, delivery_date, billing_date, payment_date))

            conn.commit()
            st.success("Transaction submitted successfully!")

        except Exception as e:
            st.error(f"An error occurred: {e}")