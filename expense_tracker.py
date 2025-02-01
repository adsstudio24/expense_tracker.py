import sqlite3
import matplotlib.pyplot as plt

DB_NAME = "expenses.db"

def init_db():
    """Ініціалізація бази даних SQLite"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_expense(category, amount, date):
    """Додає витрати до бази даних"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)", (category, amount, date))
    conn.commit()
    conn.close()
    print("✅ Витрати додано!")

def generate_report():
    """Генерує звіт витрат по категоріях"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = cursor.fetchall()
    conn.close()

    if not data:
        print("❌ Немає даних для звіту.")
        return

    categories, amounts = zip(*data)

    plt.figure(figsize=(8, 6))
    plt.pie(amounts, labels=categories, autopct="%.1f%%", startangle=140)
    plt.title("Розподіл витрат за категоріями")
    plt.show()

if __name__ == "__main__":
    init_db()
    while True:
        print("\n1. Додати витрати\n2. Генерувати звіт\n3. Вийти")
        choice = input("Виберіть опцію: ").strip()

        if choice == "1":
            category = input("Категорія витрат: ").strip()
            amount = float(input("Сума: ").strip())
            date = input("Дата (YYYY-MM-DD): ").strip()
            add_expense(category, amount, date)
        elif choice == "2":
            generate_report()
        elif choice == "3":
            print("👋 До побачення!")
            break
        else:
            print("❌ Невірний вибір. Спробуйте ще раз.")
