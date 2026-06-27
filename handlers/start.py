from utils.sender import send
from database.db import add_user


def start(message):

    chat = message["chat"]

    chat_id = chat["id"]

    name = chat.get("first_name", "User")

    add_user(chat_id, name)

    send(
        chat_id,
        f"""سلام {name} 👋

به ربات خوش آمدی.

ربات روی Railway اجرا می‌شود.
"""
    )
