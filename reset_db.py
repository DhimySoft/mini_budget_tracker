import sqlite3

DB_FILE = "budget.db"

def reset_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Drop old table if exists
    cursor.execute("DROP TABLE IF EXISTS transactions")

    # Create new table
    cursor.execute("""
        CREATE TABLE transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            amount REAL,
            category TEXT,
            description TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 30 sample transactions (20 expenses, 10 incomes)
    sample_data = [
        # Expenses
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

        # Incomes
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

    cursor.executemany("""
        INSERT INTO transactions (type, amount, category, description)
        VALUES (?, ?, ?, ?)
    """, sample_data)

    conn.commit()
    conn.close()
    print("Database reset and 30 sample transactions inserted successfully.")

if __name__ == "__main__":
    reset_db()
