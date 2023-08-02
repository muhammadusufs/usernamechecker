import logging
from utils import extract_usernames
from database import insert_username, get_all_usernames
from aiogram import Bot, Dispatcher, executor, types
from decouple import config

API_TOKEN = config("BOT_TOKEN")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Botga xush kelibsiz")



@dp.message_handler(commands=['usernames'])
async def send_usernames(message: types.Message):
    usernames = get_all_usernames()
    usernames_list = ""
    if len(usernames) > 0:
        await message.answer("Tayyorlarmoqda ...")
        for username in usernames:
            if username['is_free']:
                status = "Kanal ochilgan"
            else:
                status = "Qabul qilingan"

            usernames_list += f"@{username['username']} - {status} \n"
        
        usernames_list = usernames_list.split("\n")
        chunk_size = 10
        chunks = [usernames_list[i:i + chunk_size] for i in range(0, len(usernames_list), chunk_size)]

        for chunk in chunks:
            await message.answer("\n".join(chunk))

    else:
        await message.answer("Usernamelar mavjud emas!")


@dp.message_handler()
async def echo(message: types.Message):

    usernames = extract_usernames(message.text)
    header = "Qabul qilindi"
    usernames_list = ""
    for username in usernames:
        usernames_list += f"@{username} \n"
        insert_username(username, 0)

    usernames_list = usernames_list.split("\n")
    chunk_size = 100
    chunks = [usernames_list[i:i + chunk_size] for i in range(0, len(usernames_list), chunk_size)]

    await message.answer(header)

    for chunk in chunks:
        await message.answer("\n".join(chunk))




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
