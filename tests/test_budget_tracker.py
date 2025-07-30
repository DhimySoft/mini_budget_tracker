import sys
import os
import sqlite3
import pytest

# Ensure parent directory (project root) is in Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import core functions
from mini_budget_tracker.core import (
    init_db,
    add_expense,
    add_income,
    view_all_transactions
)

DB_FILE = "budget.db"

@pytest.fixture(autouse=True)
def setup_and_teardown():
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions")
    conn.commit()
    yield
    cursor.execute("DELETE FROM transactions")
    conn.commit()
    conn.close()

def test_add_expense(monkeypatch):
    inputs = iter(["100", "Food", "Groceries"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    add_expense()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT amount, category FROM transactions WHERE type='expense'")
    row = cursor.fetchone()
    conn.close()
    assert row == (100.0, "Food")

def test_add_income(monkeypatch):
    inputs = iter(["500", "Salary", "Monthly Pay"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    add_income()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT amount, category FROM transactions WHERE type='income'")
    row = cursor.fetchone()
    conn.close()
    assert row == (500.0, "Salary")

def test_view_all_transactions(capsys):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (type, amount, category, description) VALUES ('expense', 50, 'Food', 'Lunch')")
    cursor.execute("INSERT INTO transactions (type, amount, category, description) VALUES ('income', 1000, 'Salary', 'Job')")
    conn.commit()
    conn.close()
    view_all_transactions()
    captured = capsys.readouterr()
    assert "Food" in captured.out
    assert "Salary" in captured.out
