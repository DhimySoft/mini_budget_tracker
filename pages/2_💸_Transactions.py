import streamlit as st
import pandas as pd
from database.db import fetch_transactions, get_connection

def delete_transaction_by_id(txn_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id=?", (txn_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount

def app(currency):
    st.markdown("## 💸 Transactions")

    # fetch live transactions (no cache)
    rows = fetch_transactions()
    df = pd.DataFrame(rows, columns=["ID", "Date", "Amount", "Description", "Type", "Category"])

    if df.empty:
        st.info("No transactions yet. Add some from ➕ Add Transaction.")
        return

    # search box
    search = st.text_input("Search Description or Category")
    if search:
        df = df[df.apply(lambda row: search.lower() in row.astype(str).str.lower().to_string(), axis=1)]

    st.dataframe(df, use_container_width=True)

    st.markdown("---")
    st.subheader("Delete Transaction")

    # Select transaction ID + Description
    df["Display"] = df.apply(lambda r: f"{r['ID']} - {r['Description']}", axis=1)
    selected = st.selectbox("Select Transaction to Delete", df["Display"])

    if st.button("Delete Selected Transaction"):
        txn_id = int(selected.split(" - ")[0])
        deleted = delete_transaction_by_id(txn_id)
        if deleted:
            st.success(f"Transaction ID {txn_id} deleted successfully!")
            st.rerun()
        else:
            st.warning(f"Transaction ID {txn_id} not found!")
