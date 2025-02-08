import asyncio
from aiogram import Bot, Dispatcher
from aiogram.utils.deep_linking import create_start_link
from beanie import PydanticObjectId
from commands import all_routers
from environs import Env

env = Env()
env.read_env()


bot = Bot(token=env.str("BOT_TOKEN"))
dp = Dispatcher()
dp.include_routers(*all_routers)

async def on_startup():
    print('bot activated')


async def generate_game_link(game_id: PydanticObjectId) -> str:
    """Принимает id игры, возвращает ссылку для вступления"""

    return await create_start_link(bot, str(game_id), encode=True)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    dp.startup.register(on_startup)
    await dp.start_polling(bot, on_startup=on_startup)
    

if __name__ == "__main__":
    asyncio.run(main())
