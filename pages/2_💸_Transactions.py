import streamlit as st
import pandas as pd
from database.db import fetch_transactions

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
