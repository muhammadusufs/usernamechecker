import re
import requests
import asyncio


def extract_usernames(text):
    pattern = r'(?:(?:@|t\.me\/|https:\/\/t\.me\/)(\w+))'
    usernames = re.findall(pattern, text, re.IGNORECASE)

    return usernames


@asyncio.coroutine
def send_message(bot_token, chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
    }
    try:
        response = requests.post(url, json=data)
        return response.json() 
    except:
        return False
