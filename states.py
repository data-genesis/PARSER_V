from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):
    waiting_consent = State()
    waiting_phone = State()


class Promocode(StatesGroup):
    waiting_code = State()

