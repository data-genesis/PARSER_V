from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from config import config
from states import Registration
from keyboards import kb_consent, kb_request_contact, kb_main_menu
from api_client import api
from utils.logger import setup_logger

router = Router()
logger = setup_logger("handlers.start")


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    tg_id = message.from_user.id

    # Проверяем, зарегистрирован ли пользователь в PB
    info = await api.buyer_info_by_external_id(str(tg_id))
    if info.get("success") and info.get("is_registered"):
        await message.answer(
            "Добро пожаловать! Вы уже зарегистрированы.",
            reply_markup=kb_main_menu(),
        )
        return

    # Начинаем регистрацию
    await state.set_state(Registration.waiting_consent)
    await message.answer(
        "Начиная регистрацию, вы принимаете и соглашаетесь со следующими документами:",
        reply_markup=kb_consent(),
    )


@router.callback_query(F.data == "consent_given", Registration.waiting_consent)
async def process_consent(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Registration.waiting_phone)
    await callback.message.delete_reply_markup()
    await callback.message.answer(
        "Поделитесь, пожалуйста, вашим номером телефона.\n"
        "Нажмите на кнопку «Отправить номер».\n\n"
        "Нажимая кнопку «Отправить номер», вы даёте согласие на обработку персональных данных.",
        reply_markup=kb_request_contact(),
    )
    await callback.answer()


@router.message(F.contact, Registration.waiting_phone)
async def process_contact(message: Message, state: FSMContext):
    contact = message.contact
    phone = contact.phone_number

    # Нормализуем номер: убираем + в начале, оставляем 7XXXXXXXXXX
    phone = phone.replace("+", "").replace(" ", "").replace("-", "")
    if phone.startswith("8") and len(phone) == 11:
        phone = "7" + phone[1:]
    elif phone.startswith("9") and len(phone) == 10:
        phone = "7" + phone

    tg_id = message.from_user.id
    name = message.from_user.first_name or None
    surname = message.from_user.last_name or None

    logger.info(f"Registering buyer: tg_id={tg_id}, phone={phone}")

    result = await api.buyer_register(
        phone=phone,
        external_id=str(tg_id),
        name=name,
        surname=surname,
    )

    if result.get("success"):
        await state.clear()
        await message.answer(
            "Спасибо! Чтобы пользоваться ботом просто запустите меню, нажав на кнопку ниже\n👇",
            reply_markup=kb_main_menu(),
        )
    else:
        error_msg = result.get("message", "Неизвестная ошибка при регистрации.")
        logger.error(f"Registration failed: {result}")
        await message.answer(
            f"Ошибка регистрации: {error_msg}\nПопробуйте позже или обратитесь в поддержку.",
            reply_markup=kb_main_menu(),
        )


@router.message(Registration.waiting_phone)
async def process_contact_invalid(message: Message):
    await message.answer(
        "Пожалуйста, нажмите кнопку «📱 Отправить номер» ниже, чтобы поделиться контактом.",
        reply_markup=kb_request_contact(),
    )

