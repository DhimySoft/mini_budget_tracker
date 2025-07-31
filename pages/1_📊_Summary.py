import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from pathlib import Path


DB_FILE = Path(__file__).resolve().parent.parent / "database" / "budget.db"


def get_connection():
   return sqlite3.connect(DB_FILE, check_same_thread=False)


def app(currency):
   st.markdown(
       """
       <style>
       .kpi-card {
           background: linear-gradient(135deg, #2b5876, #4e4376);
           color: white;
           padding: 20px;
           border-radius: 10px;
           text-align: center;
           font-weight: bold;
           font-size: 1.3rem;
           box-shadow: 0 4px 10px rgba(0,0,0,0.4);
           transition: transform 0.3s ease;
       }
       .kpi-card:hover {transform: scale(1.05);}
       </style>
       """,
       unsafe_allow_html=True
   )


   st.title("📊 Summary Dashboard")


   # --- Load transactions (live, no cache) ---
   with get_connection() as conn:
       rows = conn.execute("""
           SELECT t.date, t.amount, t.description, ty.name AS type, c.name AS category
           FROM transactions t
           LEFT JOIN types ty ON t.type_id = ty.id
           LEFT JOIN categories c ON t.category_id = c.id
           ORDER BY t.date DESC
       """).fetchall()


   if not rows:
       st.info("No transactions yet. Add one using ➕ Add Transaction or restore demo data in ⚙️ Settings.")
       return


   df = pd.DataFrame(rows, columns=["Date", "Amount", "Description", "Type", "Category"])
   df["Date"] = pd.to_datetime(df["Date"])


   # --- KPI Cards ---
   total_income = df[df["Amount"] > 0]["Amount"].sum()
   total_expense = df[df["Amount"] < 0]["Amount"].sum()
   balance = total_income + total_expense


   kpi1, kpi2, kpi3 = st.columns(3)
   kpi1.markdown(f"<div class='kpi-card'>Income<br>{currency}{total_income:,.2f}</div>", unsafe_allow_html=True)
   kpi2.markdown(f"<div class='kpi-card'>Expenses<br>{currency}{total_expense:,.2f}</div>", unsafe_allow_html=True)
   kpi3.markdown(f"<div class='kpi-card'>Balance<br>{currency}{balance:,.2f}</div>", unsafe_allow_html=True)


   st.markdown("---")


   # --- Monthly Summary ---
   df["Month"] = df["Date"].dt.to_period("M").dt.to_timestamp()
   monthly_summary = df.groupby("Month")["Amount"].sum().reset_index()


   fig_monthly = px.bar(monthly_summary, x="Month", y="Amount", title="Monthly Net Amount",
                        text_auto=True, template="plotly_dark")
   fig_monthly.update_layout(height=400)
   st.plotly_chart(fig_monthly, use_container_width=True)


   # --- Category Spending (absolute sorted) ---
   cat_summary = df.groupby("Category")["Amount"].sum().reset_index()
   cat_summary["AbsAmount"] = cat_summary["Amount"].abs()
   cat_summary = cat_summary.sort_values("AbsAmount", ascending=False)


   fig_cat = px.bar(cat_summary, x="Category", y="Amount", title="Spending by Category",
                    text_auto=True, template="plotly_dark")
   fig_cat.update_layout(height=400)
   st.plotly_chart(fig_cat, use_container_width=True)

