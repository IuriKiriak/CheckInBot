import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv
from aiogram.types import ContentType
from aiogram import F

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

@dp.message(Command("get_video"))
async def send_video(message: types.Message):
    # Отправляем видео с использованием сохраненного video_id
    await message.answer("Вот видео, которое ты запросил!")
    await message.bot.send_video(message.chat.id, video_id)

# # тест получения кружков в телеграмме
# @dp.message(F.content_type == ContentType.VIDEO_NOTE)
# async def handle_video_note(message: types.Message):
#     await message.answer("Кружок принят!")

# Переменная для хранения video_id
video_id = ""

@dp.message(F.content_type == ContentType.VIDEO_NOTE)
async def handle_video_note(message: types.Message):
    video_note = message.video_note
    file_id = video_note.file_id
    duration = video_note.duration
    length = video_note.length
    file_size = video_note.file_size
    await message.answer(f"Информация о видеокружке:\n"
                         f"File ID: {file_id}\n"
                         f"Duration: {duration} сек.\n"
                         f"Length: {length} пикс.\n"
                         f"File size: {file_size} байт")



# Обработчик текстовых сообщений
@dp.message(F.content_type == ContentType.TEXT)
async def handle_text(message: types.Message):
    await message.answer(f"Ты сказал: {message.text}")

# Функция запуска бота
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
