import sqlite3
from pathlib import Path
from database.sample_data import get_demo_data

# --- Database file path ---
DB_FILE = Path(__file__).resolve().parent / "budget.db"


# --- Connection helper ---
def get_connection():
    return sqlite3.connect(DB_FILE, check_same_thread=False)


# --- Initialize DB with default tables and data ---
def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Tables
    cursor.execute("""CREATE TABLE IF NOT EXISTS types
                      (
                          id
                          INTEGER
                          PRIMARY
                          KEY
                          AUTOINCREMENT,
                          name
                          TEXT
                          UNIQUE
                          NOT
                          NULL
                      )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS categories
                      (
                          id
                          INTEGER
                          PRIMARY
                          KEY
                          AUTOINCREMENT,
                          name
                          TEXT
                          UNIQUE
                          NOT
                          NULL
                      )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS transactions
    (
        id
        INTEGER
        PRIMARY
        KEY
        AUTOINCREMENT,
        date
        TEXT
        NOT
        NULL,
        amount
        REAL
        NOT
        NULL,
        description
        TEXT,
        type_id
        INTEGER,
        category_id
        INTEGER,
        FOREIGN
        KEY
                      (
        type_id
                      ) REFERENCES types
                      (
                          id
                      ),
        FOREIGN KEY
                      (
                          category_id
                      ) REFERENCES categories
                      (
                          id
                      ))""")

    # Default types
    cursor.executemany("INSERT OR IGNORE INTO types (name) VALUES (?)",
                       [("Income",), ("Expense",)])

    # Default categories (from your diagram)
    default_categories = [
        "Rent", "Mortgage", "Communications", "Utilities", "Insurance & Fees",
        "Renovation & Repairs", "Furniture & Interior", "Garden",
        "Groceries", "Restaurants", "Coffee & Snacks", "Alcohol & Tobacco", "Bars",
        "Car & Fuel", "Public Transport", "Flights", "Taxi",
        "Clothes & Accessories", "Electronics", "Books & Games", "Gifts",
        "Culture & Events", "Hobbies", "Sports & Fitness", "Vacation",
        "Healthcare", "Pharmacy", "Eyecare", "Beauty",
        "Cash Withdrawals", "Business Expenses", "Kids", "Pets", "Charity", "Education"
    ]
    cursor.executemany("INSERT OR IGNORE INTO categories (name) VALUES (?)",
                       [(c,) for c in default_categories])

    conn.commit()
    conn.close()


# --- Fetch types & categories ---
def fetch_types():
    conn = get_connection()
    rows = conn.execute("SELECT id, name FROM types").fetchall()
    conn.close()
    return rows


def fetch_categories():
    conn = get_connection()
    rows = conn.execute("SELECT id, name FROM categories").fetchall()
    conn.close()
    return rows


# --- Insert new type/category ---
def insert_type(name):
    conn = get_connection()
    conn.execute("INSERT OR IGNORE INTO types (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()


def insert_category(name):
    conn = get_connection()
    conn.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()


def clear_all_data():
    """Delete all data from transactions, but keep types and categories intact."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions;")
    conn.commit()
    conn.close()



# --- Insert transaction ---
def insert_transaction(date, amount, description, type_id, category_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO transactions (date, amount, description, type_id, category_id)
                   VALUES (?, ?, ?, ?, ?)
                   """, (date, amount, description, type_id, category_id))
    conn.commit()
    conn.close()


# --- Fetch transactions ---
def fetch_transactions():
    conn = get_connection()
    rows = conn.execute("""
                        SELECT t.id, t.date, t.amount, t.description, ty.name AS type, c.name AS category
                        FROM transactions t
                                 LEFT JOIN types ty ON t.type_id = ty.id
                                 LEFT JOIN categories c ON t.category_id = c.id
                        ORDER BY t.date DESC
                        """).fetchall()
    conn.close()
    return rows


def generate_demo_data(n=10):
    from database.sample_data import get_demo_data

    conn = get_connection()
    cursor = conn.cursor()

    # Ensure Income & Expense types exist
    cursor.execute("INSERT OR IGNORE INTO types (name) VALUES ('Income')")
    cursor.execute("INSERT OR IGNORE INTO types (name) VALUES ('Expense')")

    # Predefined default categories
    default_categories = [
        "Salary", "Bonus", "Food", "Transport", "Health",
        "Entertainment", "Utilities"
    ]
    for cat in default_categories:
        cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (cat,))

    # Insert demo transactions
    for date, amount, desc, t_type, cat in get_demo_data(n):
        # Ensure category exists
        cursor.execute("SELECT id FROM categories WHERE name=?", (cat,))
        category_row = cursor.fetchone()
        if not category_row:
            cursor.execute("INSERT INTO categories (name) VALUES (?)", (cat,))
            category_id = cursor.lastrowid
        else:
            category_id = category_row[0]

        # Ensure type exists
        cursor.execute("SELECT id FROM types WHERE name=?", (t_type,))
        type_row = cursor.fetchone()
        if not type_row:
            cursor.execute("INSERT INTO types (name) VALUES (?)", (t_type,))
            type_id = cursor.lastrowid
        else:
            type_id = type_row[0]

        # Insert transaction
        cursor.execute("""
            INSERT INTO transactions(date, amount, description, type_id, category_id)
            VALUES (?, ?, ?, ?, ?)
        """, (date, amount, desc, type_id, category_id))

    conn.commit()
    conn.close()
