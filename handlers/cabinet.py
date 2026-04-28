from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from keyboards import kb_main_menu, kb_cabinet_actions
from api_client import api
from utils.logger import setup_logger

router = Router()
logger = setup_logger("handlers.cabinet")


@router.message(F.text == "👤 Личный кабинет")
@router.message(Command("lk"))
async def show_cabinet(message: Message):
    tg_id = message.from_user.id
    info = await api.buyer_info_by_external_id(str(tg_id))

    if not info.get("success") or not info.get("is_registered"):
        await message.answer(
            "Вы ещё не зарегистрированы. Нажмите /start для регистрации.",
            reply_markup=kb_main_menu(),
        )
        return

    phone = info.get("phone", "—")
    balance = info.get("balance", 0)
    group_name = info.get("group_name", "—")
    bonus_inactive = info.get("bonus_inactive", 0)
    next_activation = info.get("bonus_next_activation_text", "")

    text = (
        f"👤 <b>Личный кабинет</b>\n\n"
        f"📱 Телефон: <code>{phone}</code>\n"
        f"💰 Баллы: <b>{balance}</b>\n"
        f"🎖 Группа: {group_name}\n"
    )
    if bonus_inactive:
        text += f"⏳ Неактивные бонусы: {bonus_inactive}\n"
    if next_activation:
        text += f"📅 {next_activation}\n"

    await message.answer(text, reply_markup=kb_cabinet_actions())

