import streamlit as st
import time
from database.db import clear_all_data, generate_demo_data, get_connection

ADMIN_PASSWORD = "admin123"

def delete_transaction_by_id(txn_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id=?", (txn_id,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected

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

    st.title("⚙️ Settings")
    st.write("**Password protected actions**")

    password = st.text_input("Enter admin password", type="password")

    if password == ADMIN_PASSWORD:
        st.success("Access granted!")

        if st.button("Clear ALL Data"):
            clear_all_data()
            st.success("Database cleared (all tables empty).")
            time.sleep(1)
            st.rerun()

        if st.button("Restore Demo Data (10 Rows)"):
            generate_demo_data(10)
            st.success("10 demo transactions inserted successfully!")
            time.sleep(1)
            st.rerun()

        delete_id = st.number_input("Transaction ID to delete", min_value=1, step=1)
        if st.button("Delete This Transaction"):
            deleted = delete_transaction_by_id(delete_id)
            if deleted:
                st.success(f"Transaction ID {delete_id} deleted.")
            else:
                st.warning(f"No transaction found with ID {delete_id}")
    else:
        st.warning("Enter password to access data management.")
