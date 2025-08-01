import random
import datetime

def get_demo_data(num_records=1000):
    """Generate demo transactions (50% income, 50% expense)."""
    types = ["Income", "Expense"]
    categories_income = ["Salary", "Bonus"]
    categories_expense = ["Food", "Transport", "Health", "Entertainment", "Utilities"]

    data = []
    today = datetime.date.today()

    for _ in range(num_records):
        t_type = random.choice(types)
        if t_type == "Income":
            category = random.choice(categories_income)
            amount = round(random.uniform(500, 5000), 2)
        else:
            category = random.choice(categories_expense)
            amount = -round(random.uniform(20, 500), 2)

        desc = f"Auto {category}"
        date = today - datetime.timedelta(days=random.randint(0, 180))
        data.append((date.isoformat(), amount, desc, t_type, category))

    return data




