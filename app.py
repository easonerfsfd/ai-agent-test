import sqlite3

def get_user(user_input):
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE name = '" + user_input + "'"
    cursor.execute(query)
    return cursor.fetchall()

def calculate_total(items):
    total = 0
    for i in range(len(items)):
        for j in range(len(items)):
            total += items[i]
    return total
