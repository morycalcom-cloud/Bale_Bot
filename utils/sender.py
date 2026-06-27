import requests
from config import API


def send(chat_id, text):

    requests.post(
        f"{API}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text
        }
    )
