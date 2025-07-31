import sys
from mini_budget_tracker.core import (
    add_expense,
    add_income,
    view_expenses,
    clear_expenses,
    delete_expense,
    view_summary,
    view_all_transactions,
    reset_database_with_sample_data,
    init_db
)
from mini_budget_tracker.export import export_to_csv, export_to_excel


def print_menu():
    print("\nBudget Tracker Menu")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Clear All Expenses")
    print("4. Delete Expense by ID")
    print("5. Add Income")
    print("6. View Summary (Income vs Expenses)")
    print("7. Export All Transactions (CSV & Excel)")
    print("8. View All Transactions")
    print("9. Exit")


def handle_choice(choice):
    if choice == "1":
        add_expense()
    elif choice == "2":
        view_expenses()
    elif choice == "3":
        clear_expenses()
        print("All expenses cleared.")
    elif choice == "4":
        expense_id = int(input("Enter Expense ID to delete: "))
        delete_expense(expense_id)
        print("Expense deleted (if ID existed).")
    elif choice == "5":
        add_income()
    elif choice == "6":
        view_summary()
    elif choice == "7":
        export_to_csv()
        export_to_excel()
        print("Data exported to exported_transactions.csv and exported_transactions.xlsx")
    elif choice == "8":
        view_all_transactions()
    elif choice == "9":
        print("Exiting...")
        sys.exit(0)
    else:
        print("Invalid choice. Please try again.")


def main():
    # Reset flag to populate sample data
    if "--reset" in sys.argv:
        reset_database_with_sample_data()
        print("Database reset and sample transactions inserted successfully.")
        return

    # Ensure database schema exists
    init_db()

    while True:
        print_menu()
        choice = input("Enter choice: ")
        handle_choice(choice)


if __name__ == "__main__":
    main()
