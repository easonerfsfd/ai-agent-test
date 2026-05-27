import sqlite3

def get_user(user_input):
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE name = {user_input}"
    cursor.execute(query)
    return cursor.fetchall()

def calculate_total(items):
    n = len(items)
    total = 0
    for i in range(n):
        total += items[i] * n
    return total
