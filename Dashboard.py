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

st.title("Transaction Entry Dashboard")

# Form to input transaction details
with st.form("transaction_form"):
    # Buyer Details
    buyer_name = st.text_input("Buyer Name")
    buyer_address = st.text_input("Buyer Address")
    buyer_contact = st.text_input("Buyer Contact Details")

    # Printer Details
    printer_name = st.text_input("Printer Name")
    printer_address = st.text_input("Printer Address")
    printer_contact = st.text_input("Printer Contact Details")

    # Product Details
    product_desc = st.text_input("Product Description")

    # Supplier Details
    supplier_name = st.text_input("Supplier Name")
    supplier_address = st.text_input("Supplier Address")
    supplier_contact = st.text_input("Supplier Contact Details")

    # Agent Details
    agent_name = st.text_input("Agent Name")

    # Revenue Details
    price_per_item = st.number_input("Price Per Item", step=0.01, min_value=0.0)
    cost_per_item = st.number_input("Cost Per Item", step=0.01, min_value=0.0)
    print_per_item = st.number_input("Print Per Item", step=0.01, min_value=0.0)
    commission_rate = st.number_input("Commission Rate", step=0.01, min_value=0.0)
    top_up = st.number_input("Top Up Expenses", step=0.01, min_value =0.0)
    other_expenses = st.number_input("Other Expenses", step=0.01, min_value =0.0)
    quantity = st.number_input("Quantity", step=1, min_value = 0)

    quotation_num = st.text_input("Qoutation Invoice Number")

    invoice_status = st.selectbox("Invoice Status", ["Approved", "Disapproved"])

    if invoice_status == "Approved":
        # Invoice Details
        payment_request_num = st.text_input("Payment Request Invoice Number")
        delivery_client_num1 = st.text_input("Delivery Client Invoice Number - first patch")
        delivery_client_num2 = st.text_input("Delivery Client Invoice Number - second patch")
        delivery_client_num3 = st.text_input("Delivery Client Invoice Number - third patch")
        delivery_client_num4 = st.text_input("Delivery Client Invoice Number - fourth patch")
        delivery_client_num5 = st.text_input("Delivery Client Invoice Number - fifth  patch")

        billing_num = st.text_input("Billing Invoice Number")
        collection_num = st.text_input("Collection Invoice Number")
        deposit_cheque_num = st.text_input("Deposit Cheque Invoice Number")

        #Revenue Details
        production_start_date = st.text_input("Production Start Date (YYYYMMDD)")
        delivery_date_1 = st.text_input("Delivery Date - first patch (YYYYMMDD)")
        delivery_date_2 = st.text_input("Delivery Date - second patch (YYYYMMDD)")
        delivery_date_3 = st.text_input("Delivery Date - third patch (YYYYMMDD)")
        delivery_date_4 = st.text_input("Delivery Date - fourth patch (YYYYMMDD)")
        delivery_date_5 = st.text_input("Delivery Date - fifth patch (YYYYMMDD)")
        billing_date = st.text_input("Billing Date (YYYYMMDD)")
        payment_date = st.text_input("Payment Date (YYYYMMDD)")

    else:
        payment_request_num = None
        delivery_client_num1 = None
        delivery_client_num2 = None
        delivery_client_num3 = None
        delivery_client_num4 = None
        delivery_client_num5 = None
        billing_num = None
        collection_num = None
        deposit_cheque_num = None

        #Revenue Details
        production_start_date = None
        delivery_date_1 = None
        delivery_date_2 = None
        delivery_date_3 = None
        delivery_date_4 = None
        delivery_date_5 = None
        billing_date = None
        payment_date = None

    
    submitted = st.form_submit_button("Submit Transaction")

    if submitted:
        try:
            if invoice_status == "Approved":
            # Insert or get ID for Buyer
                c.execute("""
                    INSERT INTO Buyer (Name, Address, Contact_details)
                    VALUES (%s, %s, %s) ON CONFLICT (Name, Address) DO NOTHING
                """, (buyer_name, buyer_address, buyer_contact))
                conn.commit()
                c.execute("SELECT ID FROM Buyer WHERE Name = %s AND Address = %s", (buyer_name, buyer_address))
                result = c.fetchone()
                if result is None:
                    st.error("No matching record found in Buyer table.")
                    raise Exception("Buyer not found in database.")
                buyer_id = result[0]

                # Insert or get ID for Printer
                c.execute("""
                    INSERT INTO Printer (Name, Address, Contact_details)
                    VALUES (%s, %s, %s) ON CONFLICT (Name, Address) DO NOTHING
                """, (printer_name, printer_address, printer_contact))
                conn.commit()
                c.execute("SELECT ID FROM Printer WHERE Name = %s AND Address = %s", (printer_name, printer_address))
                result = c.fetchone()
                if result is None:
                    st.error("No matching record found in Printer table.")
                    raise Exception("Printer not found in database.")
                printer_id = result[0]

                # Insert or get ID for Product
                c.execute("""
                    INSERT INTO Product (Item_desc)
                    VALUES (%s) ON CONFLICT (Item_desc) DO NOTHING
                """, (product_desc,))
                conn.commit()
                c.execute("SELECT ID FROM Product WHERE Item_desc = %s", (product_desc,))
                result = c.fetchone()
                if result is None:
                    st.error("No matching record found in Product table.")
                    raise Exception("Product not found in database.")
                product_id = result[0]

                # Insert or get ID for Supplier
                c.execute("""
                    INSERT INTO Supplier (Name, Address, Contact_details)
                    VALUES (%s, %s, %s) ON CONFLICT (Name, Address) DO NOTHING
                """, (supplier_name, supplier_address, supplier_contact))
                conn.commit()
                c.execute("SELECT ID FROM Supplier WHERE Name = %s AND Address = %s", (supplier_name, supplier_address))
                result = c.fetchone()
                if result is None:
                    st.error("No matching record found in Supplier table.")
                    raise Exception("Supplier not found in database.")
                supplier_id = result[0]

                # Insert or get ID for Agent
                c.execute("""
                    INSERT INTO Agent (Name)
                    VALUES (%s) ON CONFLICT (Name) DO NOTHING
                """, (agent_name,))
                conn.commit()
                c.execute("SELECT ID FROM Agent WHERE Name = %s", (agent_name,))
                result = c.fetchone()
                if result is None:
                    st.error("No matching record found in Agent table.")
                    raise Exception("Agent not found in database.")
                agent_id = result[0]

                # Insert Invoice
                c.execute("""
                    INSERT INTO Invoice (Quotation_num, Payment_request_num, Delivery_client_num1, Delivery_client_num2, Delivery_client_num3, Delivery_client_num4, Delivery_client_num5,Billing_num, Collection_num, Deposit_cheque_num, Status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)
                    RETURNING ID
                """, (quotation_num, payment_request_num, delivery_client_num1,delivery_client_num2,delivery_client_num3,delivery_client_num4,delivery_client_num5, billing_num, collection_num, deposit_cheque_num, invoice_status))
                conn.commit()
                result = c.fetchone()
                if result is None:
                    st.error("No matching record found in Invoice table.")
                    raise Exception("Invoice not found in database.")
                invoice_id = result[0]

                # Insert into Revenue
                c.execute("""
                    INSERT INTO Revenue (ID_buyer, ID_printer, ID_product, ID_agent, ID_supplier, ID_invoice,
                                        Price_per_item, Cost_per_item, Print_per_item, Commission_rate, Top_up, 
                                        Other_expenses, Quantity, Production_start_date, Delivery_date_1, Delivery_date_2, Delivery_date_3,Delivery_date_4, Delivery_date_5,Billing_date, Payment_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (buyer_id, printer_id, product_id, agent_id, supplier_id, invoice_id,
                    price_per_item, cost_per_item, print_per_item, commission_rate,
                    top_up, other_expenses, quantity, production_start_date, delivery_date_1, delivery_date_2, delivery_date_3, delivery_date_4, delivery_date_5, billing_date, payment_date))
                conn.commit()

            else:
                c.execute("""
                    INSERT INTO Buyer (Name, Address, Contact_details)
                    VALUES (%s, %s, %s) ON CONFLICT (Name, Address) DO NOTHING
                """, (buyer_name, buyer_address, buyer_contact))
                conn.commit()
                c.execute("SELECT ID FROM Buyer WHERE Name = %s AND Address = %s", (buyer_name, buyer_address))
                result = c.fetchone()
                if result is None:
                    st.error("No matching record found in Buyer table.")
                    raise Exception("Buyer not found in database.")
                buyer_id = result[0]

                # Insert or get ID for Printer
                c.execute("""
                    INSERT INTO Printer (Name, Address, Contact_details)
                    VALUES (%s, %s, %s) ON CONFLICT (Name, Address) DO NOTHING
                """, (printer_name, printer_address, printer_contact))
                conn.commit()
                c.execute("SELECT ID FROM Printer WHERE Name = %s AND Address = %s", (printer_name, printer_address))
                result = c.fetchone()
                if result is None:
                    st.error("No matching record found in Printer table.")
                    raise Exception("Printer not found in database.")
                printer_id = result[0]

                # Insert or get ID for Product
                c.execute("""
                    INSERT INTO Product (Item_desc)
                    VALUES (%s) ON CONFLICT (Item_desc) DO NOTHING
                """, (product_desc,))
                conn.commit()
                c.execute("SELECT ID FROM Product WHERE Item_desc = %s", (product_desc,))
                result = c.fetchone()
                if result is None:
                    st.error("No matching record found in Product table.")
                    raise Exception("Product not found in database.")
                product_id = result[0]

                # Insert or get ID for Supplier
                c.execute("""
                    INSERT INTO Supplier (Name, Address, Contact_details)
                    VALUES (%s, %s, %s) ON CONFLICT (Name, Address) DO NOTHING
                """, (supplier_name, supplier_address, supplier_contact))
                conn.commit()
                c.execute("SELECT ID FROM Supplier WHERE Name = %s AND Address = %s", (supplier_name, supplier_address))
                result = c.fetchone()
                if result is None:
                    st.error("No matching record found in Supplier table.")
                    raise Exception("Supplier not found in database.")
                supplier_id = result[0]

                # Insert or get ID for Agent
                c.execute("""
                    INSERT INTO Agent (Name)
                    VALUES (%s) ON CONFLICT (Name) DO NOTHING
                """, (agent_name,))
                conn.commit()
                c.execute("SELECT ID FROM Agent WHERE Name = %s", (agent_name,))
                result = c.fetchone()
                if result is None:
                    st.error("No matching record found in Agent table.")
                    raise Exception("Agent not found in database.")
                agent_id = result[0]

                # Insert or get ID for invoice
                c.execute("""
                INSERT INTO Invoice (Quotation_num, Status)
                VALUES (%s, %s)
                RETURNING ID
                """, (quotation_num, invoice_status))
                conn.commit()
                result = c.fetchone()
                if result is None:
                    st.error("No matching record found in Invoice table.")
                    raise Exception("Invoice not found in database.")
                invoice_id = result[0]

                c.execute("""
                INSERT INTO Revenue (ID_buyer, ID_printer, ID_product, ID_agent, ID_supplier, ID_invoice,
                                        Price_per_item, Cost_per_item, Print_per_item, Commission_rate, Top_up, 
                                        Other_expenses, Quantity)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (buyer_id, printer_id, product_id, agent_id, supplier_id, invoice_id,
                    price_per_item, cost_per_item, print_per_item, commission_rate,
                    top_up, other_expenses, quantity))
                conn.commit()

                payment_request_num = None
                delivery_client_num1 = None
                delivery_client_num2 = None
                delivery_client_num3 = None
                delivery_client_num4 = None
                delivery_client_num5 = None
                billing_num = None
                collection_num = None
                deposit_cheque_num = None
                production_start_date = None
                delivery_date_1 = None
                delivery_date_2 = None
                delivery_date_3 = None
                delivery_date_4 = None
                delivery_date_5 = None
                billing_date = None
                payment_date = None
                invoice_id = None 

            st.success("Transaction submitted successfully!")

        except Exception as e:
            conn.rollback()  # Roll back transaction on error
            st.error(f"An error occurred: {e}")