import asyncio

from aiogram import Bot, Dispatcher
from aiogram.utils.deep_linking import create_start_link
from beanie import PydanticObjectId
from commands import all_routers
from environs import Env
from fastapi import FastAPI
from icecream import ic
from pydantic import AnyUrl
from uvicorn import Config, Server

env = Env()
env.read_env()

bot = Bot(token=env.str("BOT_TOKEN"))
webhook = FastAPI()


@webhook.post("/send_message")
async def send_message(chat_id: int | str, text: str):
    """Отправляет сообщение"""

    try:
        await bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        ic(e)


@webhook.get("/game_connect_link", response_model=AnyUrl)
async def game_connect_link(game_id: PydanticObjectId) -> AnyUrl:
    """Возвращает ссылку для подключения к игре"""

    return AnyUrl(await create_start_link(bot, str(game_id), encode=True))


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
