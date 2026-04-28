from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards import kb_main_menu
from handlers.start import cmd_start

router = Router()


@router.message(F.text == "🔄 /start")
async def btn_start(message: Message, state: FSMContext):
    await cmd_start(message, state)


@router.message(F.text == "🔙 Назад")
async def btn_back(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Главное меню:",
        reply_markup=kb_main_menu(),
    )

