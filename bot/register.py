from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models import User, Group
from bot.states import RegisterUser

router = Router()

print("Файл register.py загружен")

# сессии пофиксить

# Старт регистрации
@router.message(Command("reg_user"))
async def register_start(message: Message, state: FSMContext):
    print("начало регистрации!")
    await message.answer("Введите название вашей группы:")
    await state.set_state(RegisterUser.group)


# Запрашиваем ФИО после ввода группы
@router.message(RegisterUser.group)
async def register_get_group(message: Message, state: FSMContext, session: AsyncSession):
    group_name = message.text.strip()

    # Проверяем, существует ли группа
    result = await session.execute(select(Group).where(Group.name == group_name))
    group = result.scalars().first()

    if not group:
        await message.answer("Группа не найдена, попробуйте еще раз.")
        return

    await state.update_data(group_id=group.id)
    await message.answer("Теперь введите ваше ФИО (Фамилия Имя Отчество):")
    await state.set_state(RegisterUser.full_name)


# Сохраняем пользователя в БД
@router.message(RegisterUser.full_name)
async def register_get_full_name(message: Message, state: FSMContext, session: AsyncSession):
    full_name = message.text.strip()
    user_data = await state.get_data()

    # Создаем пользователя
    new_user = User(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        full_name=full_name,
        group_id=user_data["group_id"],
        role_id=2  # Например, 2 — обычный пользователь
    )

    session.add(new_user)
    await session.commit()

    await message.answer(f"Вы зарегистрированы как {full_name} в группе ID {user_data['group_id']}.")
    await state.clear()
