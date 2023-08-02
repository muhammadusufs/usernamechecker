import re
import requests
import asyncio

from decouple import config

admin_ids = config('USER_IDS')
bot_token = config('BOT_TOKEN')

def extract_usernames(text):
    pattern = r'(?:(?:@|t\.me\/|https:\/\/t\.me\/)(\w+))'
    usernames = re.findall(pattern, text, re.IGNORECASE)

    return usernames


@asyncio.coroutine
def send_message(text):
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    for admin in admin_ids.split(','):
        if admin:
            data = {
                "chat_id": admin,
                "text": text,
            }
            try:
                response = requests.post(url, json=data)
                return response.json() 
            except:
                return False