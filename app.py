from pyrogram import Client
from database import get_free_usernames, update_username_status
from utils import send_message
from decouple import config
from pyrogram.errors.exceptions.flood_420 import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import UsernameOccupied, UsernameNotOccupied, ChannelsAdminPublicTooMuch
from pyrogram.errors.exceptions.not_acceptable_406 import UserRestricted
import time

api_id = config("API_ID")
api_hash = config("API_HASH")
bot_token = config("BOT_TOKEN")
user_ids = config("USER_IDS")
request_sleep_time = config("SLEEP_TIME_EACH_REQUEST")
loop_sleep_time = config("SLEEP_TIME_EACH_LOOP")


app = Client("my_account", api_id=api_id, api_hash=api_hash)

async def check_username(username_to_check):
    try:
        chat = await app.get_chat(username_to_check)
        return True
    except UsernameNotOccupied:
        return False
    
    except:
        return True


async def main():
    async with app:

        while True:
            usernames = get_free_usernames()
            if len(usernames) > 0:
                for username in usernames:
                    res = await check_username(username_to_check=username)

                    if res == False:
                        try:
                            chan = await app.create_channel(f"@{username}", "test 123")
                            await app.set_chat_username(chan.id, username)
                            for admin in user_ids.split(','):
                                    if admin:
                                            await send_message(bot_token, admin, f"@{username} uchun kanal ochildi")
                            update_username_status(username, 1)
                            time.sleep(130)                        
                        except FloodWait as e:
                            for admin in user_ids.split(','):
                                if admin:
                                    await send_message(bot_token, admin, f"Telegram {e.value} soniya limit o'rnatdi.")
                                    print("Vaqtinchalik telegram limit qo'yildi")

                        except ChannelsAdminPublicTooMuch:
                            await send_message(bot_token, admin, f"Ushbu akkauntda juda ko'p kanallar mavjud.")
                        
                    else:
                        pass
                             

                        

                    time.sleep(float(request_sleep_time))
            time.sleep(float(loop_sleep_time))


app.run(main())
