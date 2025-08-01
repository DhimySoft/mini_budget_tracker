import streamlit as st
import importlib
from database.db import init_db

# --- Initialize DB but no auto demo ---
init_db()

def load_page(module_name):
    module = importlib.import_module(module_name)
    return module

def main():
    st.sidebar.title("Menu")
    page = st.sidebar.radio("Navigate", [
        "📊 Summary", "💸 Transactions", "➕ Add Transaction", "⚙️ Settings"
    ])
    currency = st.sidebar.selectbox("Currency", ["$", "€", "£"])

    # --- Simple header ---
    st.markdown(
        '<div style="background: linear-gradient(90deg,#4facfe,#00f2fe); '
        'padding:1rem;border-radius:10px;text-align:center;color:white;'
        'font-size:1.5rem;font-weight:bold;margin-bottom:2rem;">'
        '📈 Monthly & Annual Budget</div>',
        unsafe_allow_html=True
    )

    if page == "📊 Summary":
        load_page("pages.1_📊_Summary").app(currency)
    elif page == "💸 Transactions":
        load_page("pages.2_💸_Transactions").app(currency)
    elif page == "➕ Add Transaction":
        load_page("pages.3_➕_Add_Transaction").app(currency)
    elif page == "⚙️ Settings":
        load_page("pages.4_⚙️_Settings").app(currency)

if __name__ == "__main__":
    main()
