from aiogram import types, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import text  # Импортируем text
from db.models import Group, User
from db.db import async_session_maker


admin = Router()
print("Файл admin.py загружен")


# Обработчик команды /create_group
@admin.message(Command("create_group"))
async def create_group(message: types.Message, state: FSMContext):
    # Запрашиваем название группы
    await message.answer("Введите название новой группы:")
    await state.set_state("group_name")

@admin.message(StateFilter("group_name"))
async def handle_group_name(message: types.Message, state: FSMContext):
    group_name = message.text.strip()

    if not group_name:
        await message.answer("Название группы не может быть пустым. Попробуйте снова.")
        return

    user_id = message.from_user.id  # Telegram ID пользователя, создающего группу

    async with async_session_maker() as session:
        # Проверка, существует ли пользователь с таким ID
        result = await session.execute(text("SELECT id FROM users WHERE telegram_id = :user_id"), {'user_id': user_id})
        user = result.fetchone()

        # проверку на админа добавить
        #__________________________
        #________________________
        if not user:
            await message.answer("Ошибка: Пользователь не найден в базе данных!")
            return

        # Создаем новую группу
        new_group = Group(
            name=group_name,
            admin_id=user_id  # admin_id теперь точно существует в базе
        )

        session.add(new_group)
        await session.commit()

    await message.answer(f"Группа '{group_name}' успешно создана!")
    await state.clear()
