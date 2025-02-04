import asyncio
from aiogram import Dispatcher
from create_bot import main_bot
from commands.base import router

dp = Dispatcher()
dp.include_routers(router)


async def main():
    await main_bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(main_bot)


if __name__ == "__main__":
    asyncio.run(main())
