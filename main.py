import sqlite3
from datetime import datetime

from balethon import Client
from balethon.objects import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "YOUR_BOT_TOKEN"

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
    cur.execute(
        "INSERT OR IGNORE INTO users VALUES (?,?,?,?,0)",
        (
            user.id,
            user.first_name,
            user.username,
            str(datetime.now())
        )
    )
    db.commit()


def add_request(user_id):
    cur.execute("UPDATE users SET requests = requests + 1 WHERE id=?", (user_id,))
    db.commit()


def get_user(user_id):
    cur.execute("SELECT * FROM users WHERE id=?", (user_id,))
    return cur.fetchone()


# ---------------- MENU (Inline / Glass Buttons) ----------------

menu = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("📥 فایل‌ها", callback_data="files"),
        InlineKeyboardButton("🖼 تصویر", callback_data="image")
    ],
    [
        InlineKeyboardButton("📝 متن", callback_data="text"),
        InlineKeyboardButton("🔐 امنیت", callback_data="security")
    ],
    [
        InlineKeyboardButton("👤 پروفایل", callback_data="profile"),
        InlineKeyboardButton("ℹ️ راهنما", callback_data="help")
    ]
])


# ---------------- BOT ----------------

app = Client("bot", bot_token=TOKEN)


@app.on_message()
async def handler(client, message):

    if not message.text:
        return

    user = message.from_user
    text = message.text

    add_user(user)
    add_request(user.id)

    # START
    if text == "/start":
        await message.reply(
            f"سلام {user.first_name} 👋\nبه ربات ابزار خوش آمدی.",
            reply_markup=menu
        )

    # TEXT MENU (fallback if user types)
    elif text == "👤 پروفایل":
        u = get_user(user.id)
        await message.reply(
            f"""👤 پروفایل

🆔 {u[0]}
👤 {u[1]}
📛 {u[2]}
📅 {u[3]}
📊 {u[4]}"""
        )

    else:
        await message.reply("از منو استفاده کن 👇")


# ---------------- CALLBACK BUTTONS ----------------

@app.on_callback_query()
async def callback(client, callback):

    data = callback.data
    user = callback.from_user

    if data == "files":
        await callback.message.edit("📥 بخش فایل‌ها (نسخه بعدی)")

    elif data == "image":
        await callback.message.edit("🖼 بخش تصویر (نسخه بعدی)")

    elif data == "text":
        await callback.message.edit("📝 بخش متن (نسخه بعدی)")

    elif data == "security":
        await callback.message.edit("🔐 بخش امنیت (نسخه بعدی)")

    elif data == "profile":
        u = get_user(user.id)
        await callback.message.edit(
            f"👤 پروفایل\n\n👤 {u[1]}\n📊 {u[4]}"
        )

    elif data == "help":
        await callback.message.edit("ℹ️ راهنما: از دکمه‌ها استفاده کن")


app.run()
