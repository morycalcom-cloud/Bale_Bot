from database.db import count_users
from utils.sender import send
from config import ADMIN_ID


def admin(message):

    chat_id = message["chat"]["id"]

    if chat_id != ADMIN_ID:
        return

    send(
        chat_id,
        f"تعداد کاربران:\n{count_users()}"
    )
