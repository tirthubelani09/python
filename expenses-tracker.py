from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
import csv
import os

FILENAME = "expenses.csv"

# -------------------- Utility Functions --------------------

def validate_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False

# -------------------- Core Features --------------------

def add_expense(expenses):
    while True:
        try:
            amount = float(input("Enter amount: "))
            if amount <= 0:
                raise ValueError
            break
        except ValueError:
            print("Amount must be a positive number.")

    while True:
        date = input("Enter date (YYYY-MM-DD): ").strip()
        if validate_date(date):
            break
        print("Invalid date format.")

    category = input("Enter category: ").strip()
    description = input("Enter description: ").strip()

    expenses.append({
        "amount": amount,
        "category": category,
        "date": date,
        "description": description
    })

    print("Expense added successfully!")

def view_expenses(expenses):
    if not expenses:
        print("No expenses recorded.")
        return

    print("\n--- Expense List ---")
    for i, exp in enumerate(expenses, start=1):
        print(f"{i}. ₹{exp['amount']} | {exp['category']} | {exp['date']} | {exp['description']}")

def total_expenses(expenses):
    total = sum(exp["amount"] for exp in expenses)
    print(f"Total Expenses: ₹{total:.2f}")

def filter_by_category(expenses, category):
    category = category.lower()
    filtered = [e for e in expenses if e["category"].lower() == category]

    if not filtered:
        print("No expenses found for this category.")
        return

    for i, exp in enumerate(filtered, start=1):
        print(f"{i}. ₹{exp['amount']} | {exp['date']} | {exp['description']}")

    plot_filtered_expenses(filtered, category)

# -------------------- Plotting --------------------

def plot_filtered_expenses(expenses, category):
    totals = defaultdict(float)

    for exp in expenses:
        totals[exp["date"]] += exp["amount"]

    plt.figure()
    plt.pie(totals.values(), labels=totals.keys(), autopct="%1.1f%%", startangle=140)
    plt.title(f"Expenses for Category: {category.capitalize()}")
    plt.show()

def plot_expenses_by_category(expenses):
    totals = defaultdict(float)

    for exp in expenses:
        totals[exp["category"]] += exp["amount"]

    if not totals:
        print("No data to plot.")
        return

    plt.figure()
    plt.pie(totals.values(), labels=totals.keys(), autopct="%1.1f%%", startangle=140)
    plt.title("Expenses by Category")
    plt.show()

# -------------------- File Handling --------------------

def save_expenses(expenses):
    with open(FILENAME, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["amount", "category", "date", "description"])
        for exp in expenses:
            writer.writerow([exp["amount"], exp["category"], exp["date"], exp["description"]])

    print("Expenses saved successfully.")

def load_expenses():
    expenses = []

    if not os.path.exists(FILENAME):
        return expenses

    with open(FILENAME, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            expenses.append({
                "amount": float(row["amount"]),
                "category": row["category"],
                "date": row["date"],
                "description": row["description"]
            })

    return expenses

def delete_expense(expenses, index):
    if 1 <= index <= len(expenses):
        del expenses[index - 1]
        print("Expense deleted successfully.")
    else:
        print("Invalid index.")

# -------------------- Main Menu --------------------

def main():
    expenses = load_expenses()

    while True:
        print("\n---------------- EXPENSE TRACKER ----------------")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Total Expenses")
        print("4. Filter by Category")
        print("5. Delete Expense")
        print("6. Plot Expenses by Category")
        print("7. Save and Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            add_expense(expenses)

        elif choice == "2":
            view_expenses(expenses)

        elif choice == "3":
            total_expenses(expenses)

        elif choice == "4":
            category = input("Enter category: ")
            filter_by_category(expenses, category)

        elif choice == "5":
            try:
                index = int(input("Enter expense index: "))
                delete_expense(expenses, index)
            except ValueError:
                print("Enter a valid number.")

        elif choice == "6":
            plot_expenses_by_category(expenses)

        elif choice == "7":
            save_expenses(expenses)
            print("Thank you for using Expense Tracker.")
            break

        else:
            print("Invalid choice.")

# -------------------- Program Start --------------------

if __name__ == "__main__":
    main()