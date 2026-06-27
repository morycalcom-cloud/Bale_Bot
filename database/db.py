import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL)

with engine.begin() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS users(
            id BIGINT PRIMARY KEY,
            name TEXT
        )
    """))


def add_user(user_id, name):
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO users(id,name)
                VALUES(:id,:name)
                ON CONFLICT(id) DO NOTHING
            """),
            {"id": user_id, "name": name}
        )


def count_users():
    with engine.begin() as conn:
        return conn.execute(text("SELECT COUNT(*) FROM users")).scalar()
