import asyncio
from aiogram import Dispatcher

from bot import bot

from commands import router, on_startup

dp = Dispatcher()
dp.include_routers(router)
dp.startup.register(on_startup)



async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
