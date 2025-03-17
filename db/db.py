# db.py
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Получаем строку подключения из .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Создаем асинхронный движок SQLAlchemy
engine = create_async_engine(DATABASE_URL, echo=True)

# Создаем асинхронный sessionmaker
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Создаем базовый класс для моделей
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# Функция для получения сессии
async def get_session():
    async with async_session_maker() as session:
        yield session


from sqlalchemy.ext.asyncio import AsyncSession
from db.db import async_session_maker


# Функция для получения сессии базы данных
async def get_db_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
