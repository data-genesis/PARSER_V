# keyboards.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# Регистрация: согласие с документами
def kb_consent():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("✅ Даю согласие", callback_data="consent_given"))
    return kb

# Запрос контакта (Telegram Contact Request)
def kb_request_contact():
    kb = InlineKeyboardMarkup()
    # RequestContact работает только в ReplyKeyboard, но можно эмулировать через инструкцию
    kb.add(InlineKeyboardButton("📱 Отправить номер", callback_data="request_contact"))
    return kb

# Главное меню (после регистрации)
def kb_main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    kb.row(KeyboardButton("👤 Личный кабинет"), KeyboardButton("🎟 Активировать купон"))
    kb.row(KeyboardButton("🔄 /start"))
    return kb

# Универсальная кнопка «Назад» + /start
def kb_back_with_start():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(KeyboardButton("🔙 Назад"), KeyboardButton("🔄 /start"))
    return kb

# Личный кабинет: действия
def kb_cabinet_actions():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🎟 Активировать купон", callback_data="activate_coupon"),
        InlineKeyboardButton("🔙 Назад", callback_data="go_back")
    )
    return kb
