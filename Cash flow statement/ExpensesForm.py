import streamlit as st
import psycopg2
import pandas as pd
import numpy as np
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


# Title
st.title("Cash Flow Transactions Entry System")

# Input form
with st.form("transaction_form"):
    activity = st.text_input("Activity Name", "")
    type_ = st.selectbox("Transaction Type", ["Operating", "Investing", "Financing"])
    amount = st.number_input("Amount", step=0.01, format="%.2f")
    submitted = st.form_submit_button("Add Transaction")

    # Insert data into the database
    if submitted:
        if activity and type_ and amount:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO transactions (activity, type, amount)
                        VALUES (%s, %s, %s)
                    """, (activity, type_, amount))
                    conn.commit()
            st.success("Transaction added successfully!")
        else:
            st.error("Please fill out all fields.")