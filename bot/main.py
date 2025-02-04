import asyncio
from aiogram import Dispatcher

from bot import bot

from commands import router

dp = Dispatcher()
dp.include_routers(router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
