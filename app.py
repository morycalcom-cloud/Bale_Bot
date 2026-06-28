# app.py
import os
import requests
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text

app = Flask(__name__)

BOT_TOKEN = os.environ["BOT_TOKEN"]
DATABASE_URL = os.environ["DATABASE_URL"]
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

API = f"https://tapi.bale.ai/bot{BOT_TOKEN}"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

with engine.begin() as conn:
    conn.execute(text("""
    CREATE TABLE IF NOT EXISTS users(
        id BIGINT PRIMARY KEY,
        name TEXT
    )
    """))

def send(chat_id, txt):
    requests.post(f"{API}/sendMessage",
                  json={"chat_id": chat_id, "text": txt},
                  timeout=10)

def add_user(uid, name):
    with engine.begin() as conn:
        conn.execute(text("""
        INSERT INTO users(id,name)
        VALUES(:id,:name)
        ON CONFLICT(id) DO NOTHING
        """), {"id": uid, "name": name})

def users():
    with engine.begin() as conn:
        return conn.execute(text("SELECT COUNT(*) FROM users")).scalar()

@app.route("/")
def home():
    return "ONLINE"

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.json or {}
    msg = update.get("message")
    if not msg:
        return jsonify(ok=True)

    chat = msg["chat"]
    chat_id = chat["id"]
    name = chat.get("first_name","User")
    txt = msg.get("text","")

    add_user(chat_id, name)

    if txt == "/start":
        send(chat_id, f"سلام {name} 👋\n\nربات آماده است.\n\n/users\n/ping\n/help")
    elif txt == "/ping":
        send(chat_id, "🏓 Pong!")
    elif txt == "/help":
        send(chat_id, "دستورات:\n/start\n/ping\n/users")
    elif txt == "/users":
        if chat_id == ADMIN_ID:
            send(chat_id, f"👥 کاربران: {users()}")
        else:
            send(chat_id, "⛔ دسترسی ندارید.")
    else:
        send(chat_id, f"شما گفتید:\n\n{txt}")

    return jsonify(ok=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT",8080)))
