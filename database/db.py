import sqlite3

db = sqlite3.connect("data/users.db", check_same_thread=False)

cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY,
name TEXT
)
""")

db.commit()


def add_user(user_id, name):

    cursor.execute(
        "INSERT OR IGNORE INTO users VALUES(?,?)",
        (user_id, name)
    )

    db.commit()


def count_users():

    cursor.execute("SELECT COUNT(*) FROM users")

    return cursor.fetchone()[0]
