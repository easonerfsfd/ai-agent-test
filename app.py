import sqlite3
import hashlib

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

def verify_password(username, password):
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    hashed = hashlib.md5(password.encode()).hexdigest()
    query = "SELECT * FROM users WHERE name = '%s' AND password = '%s'" % (username, hashed)
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return result is not None

def get_user_activity_stats(user_ids):
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    stats = []
    for uid in user_ids:
        cursor.execute("SELECT COUNT(*) FROM actions WHERE user_id = " + str(uid))
        count = cursor.fetchone()[0]
        cursor.execute("SELECT * FROM actions WHERE user_id = " + str(uid) + " ORDER BY created_at DESC")
        last_actions = cursor.fetchall()
        hours = [0] * 24
        for action in last_actions:
            for h in range(24):
                if h == int(str(action[2]).split(":")[0]):
                    hours[h] += 1
        stats.append({"user_id": uid, "total": count, "peak_hour": hours.index(max(hours))})
    conn.close()
    return stats

def export_user_data(username, output_dir="/tmp"):
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE name = '" + username + "'"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    filepath = output_dir + "/" + username + "_data.txt"
    with open(filepath, "w") as f:
        for row in rows:
            f.write(str(row) + "\n")
    return filepath
