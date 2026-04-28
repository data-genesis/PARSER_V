from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def kb_consent() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Даю согласие", callback_data="consent_given")]
        ]
    )
    return kb


def kb_request_contact() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Отправить номер", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return kb


def kb_main_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👤 Личный кабинет"), KeyboardButton(text="🎟 Активировать купон")],
            [KeyboardButton(text="🔄 /start")],
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
    )
    return kb


def kb_back_with_start() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔙 Назад"), KeyboardButton(text="🔄 /start")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
    )
    return kb


def kb_cabinet_actions() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🎟 Активировать купон", callback_data="activate_coupon"),
                InlineKeyboardButton(text="🔙 Назад", callback_data="go_back"),
            ]
        ]
    )
    return kb

