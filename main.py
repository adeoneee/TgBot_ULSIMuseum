import logging
import asyncio
from aiogram import Bot, Dispatcher
from bot.handlers import register_handlers

from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=BOT_TOKEN)

    dp = Dispatcher()

    register_handlers(dp)
 
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")

if __name__ == "__main__": 
    asyncio.run(main())
