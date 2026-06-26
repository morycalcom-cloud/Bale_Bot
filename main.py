import sqlite3
from datetime import datetime
from balethon import Client, ReplyKeyboardMarkup

TOKEN = "BOT_TOKEN"

# ---------------- DB ----------------

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
        (user.id, user.first_name, user.username, str(datetime.now()))
    )
    db.commit()


def add_req(uid):
    cur.execute("UPDATE users SET requests=requests+1 WHERE id=?", (uid,))
    db.commit()


def get_user(uid):
    cur.execute("SELECT * FROM users WHERE id=?", (uid,))
    return cur.fetchone()


# ---------------- MENU ----------------

menu = ReplyKeyboardMarkup(
    keyboard=[
        ["📥 فایل‌ها", "🖼 تصویر"],
        ["📝 متن", "🔐 امنیت"],
        ["👤 پروفایل", "ℹ️ راهنما"]
    ],
    resize_keyboard=True
)

# ---------------- BOT ----------------

app = Client("bot", bot_token=TOKEN)


@app.on_message()
async def handler(client, message):

    if not message.text:
        return

    user = message.from_user
    text = message.text

    add_user(user)
    add_req(user.id)

    if text == "/start":
        await message.reply(
            f"سلام {user.first_name} 👋",
            reply_markup=menu
        )

    elif text == "👤 پروفایل":
        u = get_user(user.id)
        await message.reply(
            f"👤 پروفایل\n\n👤 {u[1]}\n📊 درخواست‌ها: {u[4]}"
        )

    elif text == "📥 فایل‌ها":
        await message.reply("🚧 بخش فایل‌ها در نسخه بعد")

    elif text == "🖼 تصویر":
        await message.reply("🚧 بخش تصویر در نسخه بعد")

    elif text == "📝 متن":
        await message.reply("🚧 بخش متن در نسخه بعد")

    elif text == "🔐 امنیت":
        await message.reply("🚧 بخش امنیت در نسخه بعد")

    else:
        await message.reply("از منو استفاده کن 👇")


app.run()
