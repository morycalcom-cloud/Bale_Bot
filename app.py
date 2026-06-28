import os
import requests
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text

app = Flask(__name__)

BOT_TOKEN = os.environ["BOT_TOKEN"]
DATABASE_URL = os.environ["DATABASE_URL"]

API = f"https://tapi.bale.ai/bot{BOT_TOKEN}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# ساخت جدول
with engine.begin() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS users(
            id BIGINT PRIMARY KEY,
            name TEXT
        )
    """))


def send(chat_id, text):
    requests.post(
        f"{API}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text
        },
        timeout=10
    )


def add_user(user_id, name):
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO users(id,name)
                VALUES(:id,:name)
                ON CONFLICT(id) DO NOTHING
            """),
            {
                "id": user_id,
                "name": name
            }
        )


def users_count():
    with engine.begin() as conn:
        return conn.execute(
            text("SELECT COUNT(*) FROM users")
        ).scalar()


@app.route("/")
def home():
    return "ONLINE"


@app.route("/webhook", methods=["POST"])
def webhook():

    update = request.json

    if not update:
        return jsonify(ok=True)

    if "message" not in update:
        return jsonify(ok=True)

    message = update["message"]

    chat = message["chat"]

    chat_id = chat["id"]

    name = chat.get("first_name", "User")

    text_msg = message.get("text", "")

    add_user(chat_id, name)

    if text_msg == "/start":

        send(
            chat_id,
            f"""سلام {name} 👋

به ربات خوش آمدی.

دستورات:

/users
/ping
/help"""
        )

    elif text_msg == "/users":

        send(
            chat_id,
            f"👥 تعداد کاربران:\n{users_count()}"
        )

    elif text_msg == "/ping":

        send(chat_id, "🏓 Pong!")

    elif text_msg == "/help":

        send(
            chat_id,
            """دستورات:

/start
/users
/ping
/help"""
        )

    else:

        send(
            chat_id,
            f"شما گفتید:\n\n{text_msg}"
        )

    return jsonify(ok=True)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8080))
    )
