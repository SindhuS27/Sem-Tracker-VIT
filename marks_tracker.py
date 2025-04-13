# 🌸 Sindhu's Personalized Semester Marks Tracker Application 🌸
# This app helps me track and store my semester marks with proper weightage calculation.
# It uses SQLite to store subject-wise marks and calculates final scores out of 100.
# Created with 💖 using Python and SQL

import sqlite3
from tabulate import tabulate

# 🌼 Connect to local SQLite database (auto-creates if not exists)
conn = sqlite3.connect('sindhu_marks.db')
cursor = conn.cursor()

# 📚 Create the marks table with proper schema
cursor.execute('''
    CREATE TABLE IF NOT EXISTS marks (
        subject TEXT PRIMARY KEY,
        cat1 INTEGER,
        cat2 INTEGER,
        fat INTEGER,
        da1 INTEGER,
        da2 INTEGER,
        da3 INTEGER,
        total REAL
    )
''')
conn.commit()

# ✨ Function to calculate weighted total (out of 100)
def calculate_total(cat1, cat2, fat, da1, da2, da3):
    return round((cat1 * 0.3) + (cat2 * 0.3) + (fat * 0.4) + da1 + da2 + da3, 2)

# 📝 Input loop for entering subject marks
num_subjects = int(input("Enter the number of subjects: "))

for _ in range(num_subjects):
    print("\nEnter details for a subject:")
    subject = input("Subject Name: ")
    cat1 = int(input("CAT 1 Marks (out of 50): "))
    cat2 = int(input("CAT 2 Marks (out of 50): "))
    fat = int(input("FAT Marks (out of 100): "))
    da1 = int(input("DA 1 Marks (out of 10): "))
    da2 = int(input("DA 2 Marks (out of 10): "))
    da3 = int(input("DA 3 Marks (out of 10): "))

    total = calculate_total(cat1, cat2, fat, da1, da2, da3)

    # 💾 Insert or update subject marks in the database
    cursor.execute('''
        INSERT INTO marks (subject, cat1, cat2, fat, da1, da2, da3, total)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(subject) DO UPDATE SET
            cat1=excluded.cat1,
            cat2=excluded.cat2,
            fat=excluded.fat,
            da1=excluded.da1,
            da2=excluded.da2,
            da3=excluded.da3,
            total=excluded.total;
    ''', (subject, cat1, cat2, fat, da1, da2, da3, total))

    conn.commit()

# 📊 Retrieve and display stored data in a table
cursor.execute("SELECT * FROM marks")
rows = cursor.fetchall()

headers = ["Subject", "CAT1", "CAT2", "FAT", "DA1", "DA2", "DA3", "Total (out of 100)"]
print("\n📌 Your Stored Semester Marks Summary 📌\n")
print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))

# 🔒 Close the connection after use
conn.close()
