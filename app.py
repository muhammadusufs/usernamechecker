from pyrogram import Client
from database import get_free_usernames, update_username_status
from utils import send_message
from decouple import config
from pyrogram.errors.exceptions.flood_420 import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import UsernameOccupied
from pyrogram.errors.exceptions.not_acceptable_406 import UserRestricted

import time

api_id = config("API_ID")
api_hash = config("API_HASH")
bot_token = config("BOT_TOKEN")
user_ids = config("USER_IDS")
request_sleep_time = config("SLEEP_TIME_EACH_REQUEST")
loop_sleep_time = config("SLEEP_TIME_EACH_LOOP")


app = Client("my_account", api_id=api_id, api_hash=api_hash)


async def main():
    async with app:
        i = 0
        free_usernames = get_free_usernames()

        if len(free_usernames) > 0:
            try:
                chan = await app.create_channel(f"test {i}", "test 123")
                channel_created = True
            except UserRestricted:
                for admin in user_ids.split(','):
                    if admin:
                        await send_message(bot_token, admin, "Ushbu telegram akkaunti orqali kanal ochish bloklangan")
                channel_created = False
        else:
            channel_created = False


        while True:

            usernames = get_free_usernames()
            if len(usernames) > 0:

                for username in usernames:
                    if channel_created == False:
                        try:
                            chan = await app.create_channel(f"test {i}", "test 123")
                            channel_created = True 
                        except UserRestricted:
                            for admin in user_ids.split(','):
                                if admin:
                                        await send_message(bot_token, admin, "Ushbu telegram akkaunti orqali kanal ochish bloklangan")
                            channel_created = False

                    if channel_created:
                        try:
                            await app.set_chat_username(chan.id, username)
                            for admin in user_ids.split(','):
                                if admin:
                                        response = await send_message(bot_token, admin, f"@{username} uchun kanal ochildi")
                            update_username_status(username, 1)
                            channel_created = False

                        except UsernameOccupied:
                            update_username_status(username, 0)
                            channel_created = True

                        except FloodWait:
                            print("Vaqtinchalik telegram limit qo'yildi")
                            print(FloodWait.MESSAGE)

                    i += 1
                    time.sleep(int(request_sleep_time))
            time.sleep(int(loop_sleep_time))
app.run(main())
