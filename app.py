import sqlite3
import hashlib
import os


def get_user(user_input):
    with sqlite3.connect("db.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE name = ?", (user_input,))
        return cursor.fetchall()


def calculate_total(items):
    return sum(items)


def verify_password(username, password):
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), b"static-salt", 100_000).hex()
    with sqlite3.connect("db.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE name = ? AND password = ?",
            (username, hashed),
        )
        return cursor.fetchone() is not None


def get_user_activity_stats(user_ids):
    if not user_ids:
        return []
    placeholders = ",".join("?" * len(user_ids))
    with sqlite3.connect("db.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT user_id, COUNT(*) FROM actions WHERE user_id IN ({placeholders}) GROUP BY user_id",
            list(user_ids),
        )
        counts = {row[0]: row[1] for row in cursor.fetchall()}
        cursor.execute(
            f"SELECT user_id, created_at FROM actions WHERE user_id IN ({placeholders}) ORDER BY created_at DESC",
            list(user_ids),
        )
        all_actions = cursor.fetchall()

    hours_map = {uid: [0] * 24 for uid in user_ids}
    for uid, ts in all_actions:
        if ts and uid in hours_map:
            try:
                h = int(str(ts).split(":")[0].split("T")[-1].split(" ")[-1])
                if 0 <= h < 24:
                    hours_map[uid][h] += 1
            except (ValueError, IndexError):
                pass

    return [
        {
            "user_id": uid,
            "total": counts.get(uid, 0),
            "peak_hour": hours_map[uid].index(max(hours_map[uid])),
        }
        for uid in user_ids
    ]


def export_user_data(username, output_dir="/tmp"):
    safe_name = os.path.basename(username)
    if not safe_name:
        raise ValueError("Invalid username")
    dest = os.path.realpath(os.path.join(output_dir, safe_name + "_data.txt"))
    if not dest.startswith(os.path.realpath(output_dir) + os.sep):
        raise ValueError("Path traversal detected")
    with sqlite3.connect("db.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE name = ?", (username,))
        rows = cursor.fetchall()
    if not rows:
        raise ValueError(f"User '{username}' not found")
    with open(dest, "w") as f:
        for row in rows:
            f.write(str(row) + "\n")
    return dest
