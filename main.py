import requests
import time

TOKEN = "BOT_TOKEN"
BASE_URL = f"https://tapi.bale.ai/bot{TOKEN}"

last_update_id = 0


def get_updates():
    global last_update_id

    url = BASE_URL + "/getUpdates"
    params = {"offset": last_update_id + 1}

    res = requests.get(url, params=params)

    print("STATUS:", res.status_code)
    print("TEXT:", res.text)   # 👈 خیلی مهم

    try:
        return res.json().get("result", [])
    except:
        return []


def send(chat_id, text):
    url = BASE_URL + "/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})


print("Bot started...")

while True:
    updates = get_updates()

    print("UPDATES:", updates)

    for u in updates:
        last_update_id = u["update_id"]

        if "message" not in u:
            continue

        msg = u["message"]
        chat_id = msg["chat"]["id"]
        text = msg.get("text", "")

        print("MESSAGE:", text)

        if text == "/start":
            send(chat_id, "سلام 👋 ربات فعاله")

    time.sleep(2)
