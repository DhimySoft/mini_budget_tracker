import streamlit as st
import datetime
from database.db import insert_transaction, fetch_types, fetch_categories

def app(currency):
    st.markdown("## ➕ Add New Transaction")

    # --- Form Fields ---
    date = st.date_input("Date", datetime.date.today())
    amount = st.number_input(f"Amount ({currency})", min_value=0.0, step=0.01)
    description = st.text_input("Description")

    # Dropdowns - fetch from DB each time (live)
    types = [t[1] for t in fetch_types()]
    if not types:
        types = ["Income", "Expense"]  # fallback
    type_choice = st.selectbox("Transaction Type", types)

    categories = [c[1] for c in fetch_categories()]
    if not categories:
        categories = ["Salary", "Food"]  # fallback
    category_choice = st.selectbox("Category", categories)

    # --- Save Transaction ---
    if st.button("Save Transaction"):
        insert_transaction(str(date), amount, description, type_choice, category_choice)
        st.success("Transaction saved successfully!")
        st.rerun()  # clear form after save
