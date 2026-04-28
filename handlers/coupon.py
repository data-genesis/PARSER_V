from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from states import Promocode
from keyboards import kb_main_menu
from api_client import api
from utils.logger import setup_logger

router = Router()
logger = setup_logger("handlers.coupon")


@router.message(F.text == "🎟 Активировать купон")
@router.message(Command("cop"))
async def start_coupon_activation(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    info = await api.buyer_info_by_external_id(str(tg_id))

    if not info.get("success") or not info.get("is_registered"):
        await message.answer(
            "Вы ещё не зарегистрированы. Нажмите /start для регистрации.",
            reply_markup=kb_main_menu(),
        )
        return

    await state.set_state(Promocode.waiting_code)
    await message.answer(
        "Введите код купона (промокода):",
        reply_markup=kb_main_menu(),
    )


@router.message(Promocode.waiting_code)
async def process_coupon_code(message: Message, state: FSMContext):
    code = message.text.strip()
    tg_id = message.from_user.id

    # Получаем телефон пользователя через API
    info = await api.buyer_info_by_external_id(str(tg_id))
    if not info.get("success") or not info.get("is_registered"):
        await state.clear()
        await message.answer(
            "Не удалось получить данные пользователя. Попробуйте /start",
            reply_markup=kb_main_menu(),
        )
        return

    phone = info.get("phone")
    if not phone:
        await state.clear()
        await message.answer(
            "Не удалось определить номер телефона. Обратитесь в поддержку.",
            reply_markup=kb_main_menu(),
        )
        return

    logger.info(f"Activating promocode: tg_id={tg_id}, phone={phone}, code={code}")
    result = await api.activate_promocode(phone=phone, code=code)

    await state.clear()

    if result.get("success"):
        await message.answer(
            f"✅ Купон <b>{code}</b> успешно активирован!",
            reply_markup=kb_main_menu(),
        )
    else:
        error_msg = result.get("message", "Не удалось активировать купон.")
        logger.error(f"Promocode activation failed: {result}")
        await message.answer(
            f"❌ Ошибка активации: {error_msg}",
            reply_markup=kb_main_menu(),
        )

