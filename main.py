import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.utils.i18n import I18n, FSMI18nMiddleware

from config import BOT_TOKEN
from handlers import rt, admin

TOKEN = BOT_TOKEN

dp = Dispatcher()


async def main() -> None:
    bot = Bot(token=TOKEN)
    dp.include_routers(rt, admin)
    i18n = I18n(path="locales", default_locale="en", domain="messages")
    dp.update.outer_middleware.register(FSMI18nMiddleware(i18n))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("EXIT")
