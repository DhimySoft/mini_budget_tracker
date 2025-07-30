import sqlite3
import csv
from rich.console import Console
from rich.table import Table

DB_FILE = "budget.db"
console = Console()

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            amount REAL,
            category TEXT,
            description TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def add_expense():
    amount = float(input("Amount: "))
    category = input("Category: ")
    description = input("Description: ")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (type, amount, category, description)
        VALUES (?, ?, ?, ?)
    """, ("expense", amount, category, description))
    conn.commit()
    conn.close()
    console.print("[green]Expense added successfully.[/green]")

def add_income():
    amount = float(input("Amount: "))
    source = input("Source: ")
    description = input("Description: ")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (type, amount, category, description)
        VALUES (?, ?, ?, ?)
    """, ("income", amount, source, description))
    conn.commit()
    conn.close()
    console.print("[green]Income added successfully.[/green]")

def view_expenses():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions WHERE type='expense'")
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        console.print("[yellow]No expenses found.[/yellow]")
        return
    table = Table(title="Expenses")
    table.add_column("ID", justify="right")
    table.add_column("Amount", justify="right")
    table.add_column("Category", justify="left")
    table.add_column("Description", justify="left")
    table.add_column("Date", justify="left")
    for row in rows:
        table.add_row(str(row[0]), f"{row[2]:.2f}", row[3], row[4], row[5])
    console.print(table)

def view_all_transactions():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        console.print("[yellow]No transactions found.[/yellow]")
        return
    table = Table(title="All Transactions")
    table.add_column("ID", justify="right")
    table.add_column("Type", justify="left")
    table.add_column("Amount", justify="right")
    table.add_column("Category", justify="left")
    table.add_column("Description", justify="left")
    table.add_column("Date", justify="left")
    for row in rows:
        table.add_row(str(row[0]), row[1], f"{row[2]:.2f}", row[3], row[4], row[5])
    console.print(table)

def delete_expense():
    expense_id = input("Enter Expense ID to delete: ")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id=? AND type='expense'", (expense_id,))
    conn.commit()
    conn.close()
    console.print("[red]Expense deleted (if ID existed).[/red]")

def clear_expenses():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE type='expense'")
    conn.commit()
    conn.close()
    console.print("[red]All expenses cleared.[/red]")

def view_summary():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='income'")
    total_income = cursor.fetchone()[0] or 0
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='expense'")
    total_expenses = cursor.fetchone()[0] or 0
    conn.close()
    balance = total_income - total_expenses
    console.print(f"\n[bold blue]Summary:[/bold blue]")
    console.print(f"Total Income:  [green]{total_income}[/green]")
    console.print(f"Total Expense: [red]{total_expenses}[/red]")
    console.print(f"Balance:       [cyan]{balance}[/cyan]")

def export_to_csv():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()
    conn.close()

    with open("exported_transactions.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Type", "Amount", "Category", "Description", "Date"])
        writer.writerows(rows)
    console.print("[green]Data exported to exported_transactions.csv[/green]")
