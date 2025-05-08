import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import ChatIdUnion
from aiogram.utils.deep_linking import create_start_link
from beanie import PydanticObjectId
from fastapi import FastAPI
from icecream import ic
from pydantic import AnyUrl
from uvicorn import Config, Server

from env import BOT_TOKEN

from .commands import all_routers
from .misc import vote_rkm
from .misc import MAIN as _

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
webhook = FastAPI()


@webhook.get("/game_connect_link", response_model=AnyUrl)
async def game_connect_link(game_id: PydanticObjectId) -> AnyUrl:
    """Возвращает ссылку для подключения к игре"""

    return AnyUrl(await create_start_link(bot, str(game_id), encode=True))


@webhook.post("/send_messages/")
async def send_messages(chats_ids_messages: dict[ChatIdUnion, str]):
    """Отправляет сообщения в чаты"""
    start_voting = all([not i[1] for i in chats_ids_messages.items()])
    for chat_id, message in chats_ids_messages.items():
        try:
            if start_voting:
                await bot.send_message(
                    chat_id=chat_id,
                    text=_["start_vote"],
                    reply_markup=vote_rkm
                )
            else:
                await bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            ic(e)


async def run_bot():
    dp = Dispatcher()
    dp.include_routers(*all_routers)
    await dp.start_polling(bot)


async def run_webhook():
    server = Server(Config("bot.main:webhook", port=8443, log_level="info"))
    await server.serve()


async def main():
    await asyncio.gather(run_webhook(), run_bot())


if __name__ == "__main__":
    asyncio.run(main())
