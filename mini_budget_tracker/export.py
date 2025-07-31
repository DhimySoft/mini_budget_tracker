# mini_budget_tracker/export.py
import pandas as pd
from pathlib import Path
from .core import get_connection
from rich.console import Console

console = Console()

def export_to_csv(filename="exported_transactions.csv"):
    conn = get_connection()
    df = pd.read_sql_query("SELECT id, type, amount, category, description, date FROM transactions", conn)
    conn.close()

    output_path = Path(filename)
    df.to_csv(output_path, index=False)
    console.print(f"[green]Data exported to {output_path}[/green]")
    return output_path

def export_to_excel(filename="exported_transactions.xlsx"):
    conn = get_connection()
    df = pd.read_sql_query("SELECT id, type, amount, category, description, date FROM transactions", conn)
    conn.close()

    output_path = Path(filename)
    df.to_excel(output_path, index=False)
    console.print(f"[green]Data exported to {output_path}[/green]")
    return output_path
