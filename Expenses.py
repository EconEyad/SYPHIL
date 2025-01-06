import streamlit as st
import psycopg2
from urllib.parse import urlparse

st.title("Cash Flow Data Entry")

# Form to input cash flow data
with st.form("cash_flow_form"):
    # Investing Activities Section
    st.markdown("## Investing Activities")
    capital_expenditures = st.number_input("Capital Expenditures", step=0.01, format="%.2f")
    
    st.markdown("---")

    # Financing Activities Section
    st.markdown("## Financing Activities")
    repayment_of_loans = st.number_input("Repayment of Loans", step=0.01, format="%.2f")
    st.markdown("---")

    # Personal Activities Section
    st.markdown("## Personal Expenses")
    personal = st.number_input("Personal Expenses", step = 0.01, format ="%.2f")
    st.markdown("---")

    # Salary
    st.markdown("## Salary")
    salary = st.number_input("Salary", step =0.01, format = "%.2f")
    st.markdown("---")

    # Submit Button
    submitted = st.form_submit_button("Submit Cash Flow Data")
