import streamlit as st
import importlib
from database.db import init_db, reset_and_restore_demo


# ------------------- INITIALIZATION -------------------
# Initialize DB and restore demo data if empty
init_db()
reset_and_restore_demo()


# ------------------- CUSTOM CSS -------------------
st.markdown(
   """
   <style>
       /* Gradient background for the header */
       .header-gradient {
           background: linear-gradient(90deg, #ff7eb3, #ff758c, #ff7eb3);
           padding: 1rem;
           border-radius: 10px;
           text-align: center;
           color: white;
           font-size: 1.5rem;
           font-weight: bold;
           margin-bottom: 2rem;
       }
       /* KPI card styling */
       .stMetric {
           background: #262730;
           border-radius: 12px;
           padding: 1rem !important;
           box-shadow: 0 4px 10px rgba(0,0,0,0.3);
       }
   </style>
   """,
   unsafe_allow_html=True
)


# ------------------- PAGE LOADER -------------------
def load_page(module_name):
   module = importlib.import_module(module_name)
   return module


def main():
   st.sidebar.title("Menu")
   page = st.sidebar.radio("Navigate", [
       "📊 Summary",
       "💸 Transactions",
       "➕ Add Transaction",
       "⚙️ Settings"
   ])
   currency = st.sidebar.selectbox("Currency", ["$", "€", "£"])


   # Gradient Header
   st.markdown('<div class="header-gradient">📈 Monthly & Annual Budget</div>', unsafe_allow_html=True)


   # Load appropriate page
   if page == "📊 Summary":
       load_page("pages.1_📊_Summary").app(currency)
   elif page == "💸 Transactions":
       load_page("pages.2_💸_Transactions").app(currency)
   elif page == "➕ Add Transaction":
       load_page("pages.3_➕_Add_Transaction").app(currency)
   elif page == "⚙️ Settings":
       load_page("pages.4_⚙️_Settings").app(currency)
       # After reset, refresh page automatically
       st.rerun()


if __name__ == "__main__":
   main()

