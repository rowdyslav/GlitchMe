import asyncio

from aiogram import Dispatcher
from commands.base import router
from core import bot

dp = Dispatcher()
dp.include_routers(router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
