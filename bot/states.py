from aiogram.fsm.state import StatesGroup, State

class RegisterUser(StatesGroup):
    group = State()
    full_name = State()
