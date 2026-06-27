from utils.sender import send


def echo(message):

    chat_id = message["chat"]["id"]

    text = message.get("text", "")

    send(chat_id, f"شما گفتید:\n\n{text}")
