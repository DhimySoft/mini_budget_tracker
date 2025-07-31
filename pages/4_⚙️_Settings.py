import streamlit as st
import time
from database.db import get_connection, insert_category, insert_type
from database.sample_data import get_demo_data

# --- Clear All Tables ---
def clear_all_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript("""
        DELETE FROM transactions;
        DELETE FROM types;
        DELETE FROM categories;
    """)
    conn.commit()
    conn.close()

# --- Generate Demo Data ---
def generate_demo_data(n=1000):
    conn = get_connection()
    cursor = conn.cursor()

    default_types = ["Income", "Expense"]
    default_categories = ["Salary", "Bonus", "Food", "Transport", "Health", "Entertainment", "Utilities"]

    for t in default_types:
        cursor.execute("INSERT OR IGNORE INTO types (name) VALUES (?);", (t,))
    for c in default_categories:
        cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?);", (c,))

    cursor.execute("SELECT name, id FROM types;")
    type_map = dict(cursor.fetchall())
    cursor.execute("SELECT name, id FROM categories;")
    cat_map = dict(cursor.fetchall())

    demo_data = get_demo_data(n)
    for date, amount, desc, t_type, cat in demo_data:
        cursor.execute("""
            INSERT INTO transactions (date, amount, description, type_id, category_id)
            VALUES (?, ?, ?, ?, ?)
        """, (date, amount, desc, type_map[t_type], cat_map.get(cat, 1)))

    conn.commit()
    conn.close()

# --- Settings Page ---
def app(currency):
    st.markdown("""
        <style>
        .title {font-size: 2rem; font-weight: 700;}
        .section-header {margin-top: 30px; font-size: 1.2rem; font-weight: 600; color: #f1f1f1;}
        .stButton>button {background-color: #FF4B4B; color: white; font-weight: bold;
                          border-radius: 8px; padding: 0.5rem 1rem;}
        .stButton>button:hover {background-color: #ff2e2e;}
        input, textarea {background-color: #1E1E1E !important; color: white !important;}
        </style>
        """, unsafe_allow_html=True)

    st.markdown('<p class="title">⚙️ Settings</p>', unsafe_allow_html=True)

    # ---- Reset & Restore Demo Data ----
    st.markdown('<p class="section-header">Database Management</p>', unsafe_allow_html=True)
    if st.button("Reset & Restore Demo Data (1000 Rows)"):
        clear_all_data()
        generate_demo_data(1000)
        st.success("Database reset and 1000 demo transactions restored successfully!")
        time.sleep(1)
        st.rerun()

    # ---- Add New Category ----
    st.markdown('<p class="section-header">Add New Category</p>', unsafe_allow_html=True)
    new_category = st.text_input("Category Name")
    if st.button("Save Category"):
        if new_category.strip():
            insert_category(new_category.strip())
            st.success(f"Category '{new_category}' added successfully!")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Category name cannot be empty.")

    # ---- Add New Transaction Type ----
    st.markdown('<p class="section-header">Add New Transaction Type</p>', unsafe_allow_html=True)
    new_type = st.text_input("Transaction Type Name")
    if st.button("Save Transaction Type"):
        if new_type.strip():
            insert_type(new_type.strip())
            st.success(f"Transaction type '{new_type}' added successfully!")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Transaction type name cannot be empty.")
