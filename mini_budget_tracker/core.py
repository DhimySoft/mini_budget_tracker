import sqlite3
import csv
from pathlib import Path
from rich.console import Console
from rich.table import Table
import os

# Use local persistent database file
DB_FILE = os.environ.get("DB_FILE", "budget.db")
console = Console()

def get_connection():
    return sqlite3.connect(DB_FILE)

def init_db():
    conn = get_connection()
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

# ---------- Add Expense ----------
def add_expense(amount=None, category=None, description=None):
    """Supports both CLI (interactive) and direct test calls (with args)."""
    if amount is None or category is None or description is None:
        amount = float(input("Amount: "))
        category = input("Category: ")
        description = input("Description: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transactions (type, amount, category, description) VALUES (?, ?, ?, ?)",
        ("expense", amount, category, description)
    )
    conn.commit()
    conn.close()
    console.print("[green]Expense added successfully.[/green]")
    return (amount, category)  # <-- tests expect this tuple

# ---------- Add Income ----------
def add_income(amount=None, category=None, description=None):
    """Supports both CLI (interactive) and direct test calls (with args)."""
    if amount is None or category is None or description is None:
        amount = float(input("Amount: "))
        category = input("Category: ")
        description = input("Description: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transactions (type, amount, category, description) VALUES (?, ?, ?, ?)",
        ("income", amount, category, description)
    )
    conn.commit()
    conn.close()
    console.print("[green]Income added successfully.[/green]")
    return (amount, category)  # <-- tests expect this tuple

# ---------- View Expenses ----------
def view_expenses():
    conn = get_connection()
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

# ---------- View All Transactions ----------
def view_all_transactions():
    conn = get_connection()
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

# ---------- Delete Expense ----------
def delete_expense(expense_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id=? AND type='expense'", (expense_id,))
    conn.commit()
    conn.close()

# ---------- Clear Expenses ----------
def clear_expenses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE type='expense'")
    conn.commit()
    conn.close()

# ---------- Summary ----------
def view_summary():
    conn = get_connection()
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

# ---------- Export Transactions ----------
def export_all_transactions(filename="exported_transactions.csv"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, type, amount, category, description, date FROM transactions")
    rows = cursor.fetchall()
    conn.close()
    headers = ["ID", "Type", "Amount", "Category", "Description", "Date"]
    with open(Path(filename), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    return filename

# ---------- Reset with 30 Sample Transactions ----------
def reset_database_with_sample_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS transactions")
    conn.commit()
    init_db()
    sample_data = [
        ("expense", 50.0, "Food", "Lunch at restaurant"),
        ("expense", 25.5, "Transport", "Subway fare"),
        ("expense", 75.0, "Groceries", "Supermarket shopping"),
        ("expense", 100.0, "Utilities", "Electricity bill"),
        ("expense", 40.0, "Entertainment", "Movie night"),
        ("expense", 60.0, "Health", "Pharmacy purchase"),
        ("expense", 20.0, "Transport", "Bus fare"),
        ("expense", 45.0, "Food", "Dinner takeout"),
        ("expense", 30.0, "Groceries", "Farmer's market"),
        ("expense", 55.0, "Entertainment", "Concert ticket"),
        ("expense", 12.0, "Transport", "Taxi"),
        ("expense", 70.0, "Food", "Brunch"),
        ("expense", 90.0, "Utilities", "Water bill"),
        ("expense", 35.0, "Groceries", "Bakery items"),
        ("expense", 110.0, "Rent", "Extra charge"),
        ("expense", 15.0, "Entertainment", "Video rental"),
        ("expense", 25.0, "Health", "Vitamins"),
        ("expense", 8.0, "Food", "Coffee shop"),
        ("expense", 12.5, "Transport", "Uber ride"),
        ("expense", 95.0, "Groceries", "Monthly bulk purchase"),
        ("income", 1500.0, "Salary", "Monthly salary"),
        ("income", 200.0, "Freelance", "Project A"),
        ("income", 100.0, "Gift", "Birthday gift"),
        ("income", 50.0, "Cashback", "Credit card cashback"),
        ("income", 300.0, "Side hustle", "Weekend job"),
        ("income", 400.0, "Investments", "Dividends"),
        ("income", 120.0, "Refund", "Product return"),
        ("income", 60.0, "Interest", "Bank savings"),
        ("income", 250.0, "Freelance", "Project B"),
        ("income", 80.0, "Other", "Misc income")
    ]
    cursor.executemany(
        "INSERT INTO transactions (type, amount, category, description) VALUES (?, ?, ?, ?)",
        sample_data
    )
    conn.commit()
    conn.close()
