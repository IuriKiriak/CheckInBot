from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

# Создаем базовый класс для всех моделей
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(255), nullable=True)
    full_name = Column(String(255), nullable=True)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=True)

    role = relationship("Role", back_populates="users")
    group = relationship("Group", back_populates="users", foreign_keys=[group_id])  # Указываем foreign_keys для этого отношения

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, full_name={self.full_name})>"

class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=True)
    admin_id = Column(Integer, ForeignKey('users.telegram_id'), nullable=False)  # Ссылаемся на telegram_id

    admin = relationship("User", back_populates="admin_group", foreign_keys=[admin_id])  # Указываем foreign_keys для этого отношения
    users = relationship("User", back_populates="group", foreign_keys=[User.group_id])  # Указываем, что связь с группой идет через group_id в таблице users

    def __repr__(self):
        return f"<Group(id={self.id}, name={self.name})>"




class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)

    users = relationship("User", back_populates="role")

    def __repr__(self):
        return f"<Role(id={self.id}, name={self.name})>"

class Checkin(Base):
    __tablename__ = 'checkins'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    video_id = Column(String(255), nullable=True)  # Assuming video_id is a string (file_id from Telegram)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    check = Column(Boolean, nullable=False, default=False)

    user = relationship("User", back_populates="checkins")
    group = relationship("Group", back_populates="checkins")

    def __repr__(self):
        return f"<Checkin(id={self.id}, user_id={self.user_id}, group_id={self.group_id}, check={self.check})>"

# Обратные связи
User.admin_group = relationship("Group", back_populates="admin", foreign_keys=[Group.admin_id])
Group.checkins = relationship("Checkin", back_populates="group")
User.checkins = relationship("Checkin", back_populates="user")
