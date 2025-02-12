import asyncio

from aiogram import Bot, Dispatcher
from commands import all_routers
from environs import Env
from fastapi import FastAPI
from icecream import ic
from uvicorn import Config, Server
from misc.link import generate_game_link
from beanie import PydanticObjectId

env = Env()
env.read_env()

bot = Bot(token=env.str("BOT_TOKEN"))
webhook = FastAPI()


@webhook.post("/send-message/")
async def send_message(chat_id: str, text: str):
    """Отправляет сообщение для post запроса в params передать chat_id, text"""

    try:
        await bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        ic(e)


@webhook.get("/get-link/")
async def get_link(game_id: PydanticObjectId):
    """отправляет ссылку для подключения к игре"""

    try:
        return await generate_game_link(bot, game_id)
    except Exception as e:
        ic(e)


async def run_bot():
    dp = Dispatcher()
    dp.include_routers(*all_routers)
    await dp.start_polling(bot)


async def run_webhook():
    server = Server(Config("main:webhook", port=5000, log_level="info"))
    await server.serve()


async def main():
    await asyncio.gather(run_webhook(), run_bot())


if __name__ == "__main__":
    asyncio.run(main())
