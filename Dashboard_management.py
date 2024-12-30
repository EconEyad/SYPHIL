import streamlit as st
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('Transaction.sqlite3')
conn.execute("PRAGMA foreign_keys = ON;")  # Enable foreign key constraints
c = conn.cursor()

st.title("Manage Transactions Dashboard")

# Select table to manage
table = st.selectbox("Select Table to Manage", ["Printer", "Revenue", "Buyer", "Supplier", "Agent", "Invoice", "Date"])

# Load and display data
st.subheader(f"Entries in {table} Table")
query = f"SELECT * FROM {table}"
data = pd.read_sql(query, conn)
st.dataframe(data)

# Allow user to select a row for deletion
st.subheader(f"Delete an Entry from {table}")
selected_id = st.selectbox("Select ID to Delete", data['ID'] if not data.empty else [])

if st.button("Delete Entry"):
    if selected_id:
        try:
            # Delete the selected entry
            c.execute(f"DELETE FROM {table} WHERE ID = ?", (selected_id,))
            conn.commit()
            st.success(f"Entry with ID {selected_id} successfully deleted.")
            
            # Refresh the displayed data
            data = pd.read_sql(query, conn)
            st.dataframe(data)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("No ID selected.")

conn.close()