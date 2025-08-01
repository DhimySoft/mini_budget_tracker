import streamlit as st
import datetime
from database.db import insert_transaction, fetch_types, fetch_categories, insert_type, insert_category

def app(currency):
    # --- Unified Gradient Header ---
    st.markdown("""
        <div style="background: linear-gradient(90deg, #4facfe, #43e97b, #f8ffae, #f093fb, #f5576c);
                    padding: 1rem; border-radius: 15px; text-align: center; 
                    font-size: 1.5rem; font-weight: bold; color: white;">
            📈 Monthly & Annual Budget
        </div>
        <br>
    """, unsafe_allow_html=True)

    st.markdown("## ➕ Add New Transaction")

    date = st.date_input("Date", datetime.date.today())
    amount = st.number_input(f"Amount ({currency})", step=0.01)
    description = st.text_input("Description")

    # --- Type selection ---
    types = fetch_types()
    type_names = sorted([t[1] for t in types]) + ["➕ Add New Type"]
    type_choice = st.selectbox("Transaction Type", type_names)
    if type_choice == "➕ Add New Type":
        new_type = st.text_input("Enter new type name")
        if st.button("Save New Type"):
            insert_type(new_type)
            st.success(f"Type '{new_type}' added!")
            st.rerun()
        return

    # --- Category selection ---
    categories = fetch_categories()
    category_names = sorted([c[1] for c in categories]) + ["➕ Add New Category"]
    category_choice = st.selectbox("Category", category_names)
    if category_choice == "➕ Add New Category":
        new_category = st.text_input("Enter new category name")
        if st.button("Save New Category"):
            insert_category(new_category)
            st.success(f"Category '{new_category}' added!")
            st.rerun()
        return

    # --- ID lookup ---
    type_id = next(t[0] for t in types if t[1] == type_choice)
    category_id = next(c[0] for c in categories if c[1] == category_choice)

    # --- Auto negative ---
    if type_choice.lower() == "expense" and amount > 0:
        amount = -amount

    if st.button("Save Transaction"):
        insert_transaction(str(date), amount, description, type_id, category_id)
        st.success("Transaction saved successfully!")
        st.rerun()
