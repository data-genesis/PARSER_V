import asyncio
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config import config
from handlers import start, cabinet, coupon, navigation
from middlewares.user_middleware import UserMiddleware
from api_client import api
from utils.logger import setup_logger

logger = setup_logger("bot")


def main() -> None:
    bot = Bot(token=config.TG_BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    # Регистрация middleware
    dp.message.middleware(UserMiddleware())
    dp.callback_query.middleware(UserMiddleware())

    # Подключение роутеров
    dp.include_router(start.router)
    dp.include_router(cabinet.router)
    dp.include_router(coupon.router)
    dp.include_router(navigation.router)

    logger.info("Bot started")
    try:
        dp.run_polling(bot)
    finally:
        asyncio.run(api.close())
        logger.info("Bot stopped")


if __name__ == "__main__":
    main()

