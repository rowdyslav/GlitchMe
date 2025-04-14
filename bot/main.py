import asyncio

from aiogram import Bot, Dispatcher
from aiogram.utils.deep_linking import create_start_link
from beanie import PydanticObjectId
from fastapi import FastAPI
from icecream import ic
from pydantic import AnyUrl
from uvicorn import Config, Server
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from .commands.keyboard import players_vote_kb
from env import BOT_TOKEN

from .commands import all_routers

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
webhook = FastAPI()


@webhook.post("/send_message")
async def send_message(chat_id: int | str, text: str):
    """Отправляет сообщение"""

    try:
        await bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        ic(e)


@webhook.post("/send_messages")
async def send_messages(chat_ids: dict[str, str]):
    """Отправляет сообщения, в json принимает dict[chat_id:str, text:str]"""

    for chat_id in chat_ids:
        try:
            await bot.send_message(chat_id=chat_id, text=chat_ids[chat_id])
        except Exception as e:
            ic(e)


@webhook.get("/game_connect_link", response_model=AnyUrl)
async def game_connect_link(game_id: PydanticObjectId) -> AnyUrl:
    """Возвращает ссылку для подключения к игре"""

    return AnyUrl(await create_start_link(bot, str(game_id), encode=True))


@webhook.post("/start_vote")
async def start_vote(players: list[dict[str, str]]) -> AnyUrl:
    """Голосование за исключение игрока
    список словарей с ключами name и id
    рассылается всем кто в игре"""

    for player in players:
        try:
            await bot.send_message(
                chat_id=player["id"],
                text="Выбирайте с умом",
                reply_markup=players_vote_kb(players),
            )
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
