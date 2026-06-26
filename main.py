from flask import Flask, request
import requests
import sqlite3
from datetime import datetime

TOKEN = "YOUR_BALE_BOT_TOKEN"
BASE_URL = f"https://tapi.bale.ai/bot{TOKEN}"

app = Flask(__name__)

# ---------------- DATABASE ----------------

db = sqlite3.connect("users.db", check_same_thread=False)
cur = db.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY,
first_name TEXT,
username TEXT,
join_date TEXT,
requests INTEGER DEFAULT 0
)
""")
db.commit()


def add_user(user):
    cur.execute("""
    INSERT OR IGNORE INTO users VALUES (?,?,?,?,0)
    """, (
        user["id"],
        user.get("first_name"),
        user.get("username"),
        str(datetime.now())
    ))
    db.commit()


def add_req(uid):
    cur.execute("UPDATE users SET requests=requests+1 WHERE id=?", (uid,))
    db.commit()


def get_user(uid):
    cur.execute("SELECT * FROM users WHERE id=?", (uid,))
    return cur.fetchone()


# ---------------- SEND MESSAGE ----------------

def send_message(chat_id, text):
    requests.post(BASE_URL + "/sendMessage", json={
        "chat_id": chat_id,
        "text": text
    })


def edit_message(chat_id, text, message_id):
    requests.post(BASE_URL + "/editMessageText", json={
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text
    })


# ---------------- INLINE MENU ----------------

def menu():
    return {
        "inline_keyboard": [
            [
                {"text": "📥 فایل‌ها", "callback_data": "files"},
                {"text": "🖼 تصویر", "callback_data": "image"}
            ],
            [
                {"text": "📝 متن", "callback_data": "text"},
                {"text": "🔐 امنیت", "callback_data": "security"}
            ],
            [
                {"text": "👤 پروفایل", "callback_data": "profile"},
                {"text": "ℹ️ راهنما", "callback_data": "help"}
            ]
        ]
    }


# ---------------- WEBHOOK ----------------

@app.route("/", methods=["GET"])
def home():
    return "Bot is running"


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json

    # ---------------- MESSAGE ----------------
    if "message" in data:

        msg = data["message"]
        chat_id = msg["chat"]["id"]
        user = msg["from"]
        text = msg.get("text", "")

        add_user(user)
        add_req(user["id"])

        if text == "/start":
            requests.post(BASE_URL + "/sendMessage", json={
                "chat_id": chat_id,
                "text": "👋 خوش آمدی به ربات حرفه‌ای",
                "reply_markup": menu()
            })

        elif text == "👤 پروفایل":
            u = get_user(user["id"])
            send_message(chat_id,
                f"""👤 پروفایل

🆔 {u[0]}
👤 {u[1]}
📛 {u[2]}
📅 {u[3]}
📊 {u[4]}"""
            )

        else:
            send_message(chat_id, "از منو استفاده کن 👇")

    # ---------------- CALLBACK ----------------
    elif "callback_query" in data:

        cb = data["callback_query"]
        chat_id = cb["message"]["chat"]["id"]
        msg_id = cb["message"]["message_id"]
        user_id = cb["from"]["id"]
        data_cb = cb["data"]

        add_req(user_id)

        if data_cb == "files":
            edit_message(chat_id, "📥 بخش فایل‌ها (نسخه بعد)", msg_id)

        elif data_cb == "image":
            edit_message(chat_id, "🖼 بخش تصویر (نسخه بعد)", msg_id)

        elif data_cb == "text":
            edit_message(chat_id, "📝 بخش متن (نسخه بعد)", msg_id)

        elif data_cb == "security":
            edit_message(chat_id, "🔐 بخش امنیت (نسخه بعد)", msg_id)

        elif data_cb == "profile":
            u = get_user(user_id)
            edit_message(chat_id,
                f"👤 پروفایل\n\n👤 {u[1]}\n📊 درخواست‌ها: {u[4]}",
                msg_id
            )

        elif data_cb == "help":
            edit_message(chat_id, "ℹ️ از منو استفاده کن", msg_id)

    return "ok"


# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
