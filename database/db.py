import sqlite3
from pathlib import Path
from database.sample_data import get_demo_data


DB_FILE = Path(__file__).resolve().parent / "budget.db"


def get_connection():
   return sqlite3.connect(DB_FILE, check_same_thread=False)


def init_db():
   conn = get_connection()
   cursor = conn.cursor()
   cursor.execute("""CREATE TABLE IF NOT EXISTS types(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT UNIQUE NOT NULL)""")
   cursor.execute("""CREATE TABLE IF NOT EXISTS categories(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT UNIQUE NOT NULL)""")
   cursor.execute("""CREATE TABLE IF NOT EXISTS transactions(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       date TEXT NOT NULL,
                       amount REAL NOT NULL,
                       description TEXT,
                       type_id INTEGER,
                       category_id INTEGER,
                       FOREIGN KEY (type_id) REFERENCES types(id),
                       FOREIGN KEY (category_id) REFERENCES categories(id))""")
   conn.commit()
   conn.close()


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


def insert_transaction(date, amount, description, type_id, category_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO transactions (date, amount, description, type_id, category_id)
        VALUES (?, ?, ?, ?, ?)
        """,
        (date, amount, description, type_id, category_id),
    )
    conn.commit()
    conn.close()

def fetch_transactions():
   conn = get_connection()
   rows = conn.execute("""SELECT t.id, t.date, t.amount, t.description, ty.name, c.name
                          FROM transactions t
                          LEFT JOIN types ty ON t.type_id = ty.id
                          LEFT JOIN categories c ON t.category_id = c.id
                          ORDER BY t.date DESC""").fetchall()
   conn.close()
   return rows


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


def clear_all_data():
   conn = get_connection()
   conn.execute("DELETE FROM transactions; DELETE FROM types; DELETE FROM categories;")
   conn.commit()
   conn.close()


def generate_demo_data():
   conn = get_connection()
   cursor = conn.cursor()
   types = ["Income", "Expense"]
   categories = ["Salary", "Bonus", "Food", "Transport", "Health", "Entertainment", "Utilities"]
   for t in types:
       cursor.execute("INSERT OR IGNORE INTO types(name) VALUES (?)", (t,))
   for c in categories:
       cursor.execute("INSERT OR IGNORE INTO categories(name) VALUES (?)", (c,))
   type_map = dict(cursor.execute("SELECT name,id FROM types").fetchall())
   cat_map = dict(cursor.execute("SELECT name,id FROM categories").fetchall())


   for date, amount, desc, t_type, cat in get_demo_data(1000):
       if cat not in cat_map:
           cursor.execute("INSERT INTO categories(name) VALUES (?)", (cat,))
           cat_map[cat] = cursor.lastrowid
       cursor.execute("""INSERT INTO transactions(date, amount, description, type_id, category_id)
                         VALUES (?, ?, ?, ?, ?)""",
                      (date, amount, desc, type_map[t_type], cat_map[cat]))
   conn.commit()
   conn.close()


def reset_and_restore_demo():
   conn = get_connection()
   cursor = conn.cursor()
   cursor.execute("DROP TABLE IF EXISTS transactions;")
   cursor.execute("DROP TABLE IF EXISTS types;")
   cursor.execute("DROP TABLE IF EXISTS categories;")
   conn.commit()
   conn.close()
   init_db()
   generate_demo_data()




def insert_transaction(date, amount, description, type_id, category_id):
   conn = get_connection()
   cursor = conn.cursor()
   cursor.execute(
       """
       INSERT INTO transactions (date, amount, description, type_id, category_id)
       VALUES (?, ?, ?, ?, ?)
       """,
       (date, amount, description, type_id, category_id)
   )
   conn.commit()  # <-- This is required
   conn.close()