import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv

import os

load_dotenv()

TOKEN = os.getenv("TOKENTELEGRAMBOT")

# Создаём объект бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет! Я Telegram-бот на aiogram 🚀")

# Обработчик текстовых сообщений
@dp.message()
async def echo_handler(message: Message):
    await message.answer(f"Ты сказал: {message.text}")

# Функция запуска бота
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
