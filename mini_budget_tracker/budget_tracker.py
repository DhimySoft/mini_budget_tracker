from . import core as bt

def main():
    bt.init_db()
    while True:
        print("\nBudget Tracker Menu")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Clear All Expenses")
        print("4. Delete Expense by ID")
        print("5. Add Income")
        print("6. View Summary (Income vs Expenses)")
        print("7. Export All Transactions to CSV")
        print("8. View All Transactions")
        print("9. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            bt.add_expense()
        elif choice == "2":
            bt.view_expenses()
        elif choice == "3":
            bt.clear_expenses()
        elif choice == "4":
            bt.delete_expense()
        elif choice == "5":
            bt.add_income()
        elif choice == "6":
            bt.view_summary()
        elif choice == "7":
            bt.export_to_csv()
        elif choice == "8":
            bt.view_all_transactions()
        elif choice == "9":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
