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
from .misc import MAIN as _
from .misc import vote_rkm, player_vote_ikm

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
webhook = FastAPI()


@webhook.get("/game_connect_link", response_model=AnyUrl)
async def game_connect_link(game_id: PydanticObjectId) -> AnyUrl:
    """Возвращает ссылку для подключения к игре"""

    return AnyUrl(await create_start_link(bot, str(game_id), encode=True))


@webhook.post("/send_messages/")
async def send_messages(players_data: list[tuple],):
    """Отправляет сообщения в чаты
    tuple[tg_id, name, alive, message]"""

    no_messages = all([i[3] is None for i in players_data.items()])
    if no_messages:
        messages_kwargs = []
        for player in players_data:
            tg_id, alive = player[0], player[2]
            other_players = [
                {
                "tg_id" : p[0],
                "name" : p[1],
                "alive" : p[2]
                }for p in players_data if p["tg_id"] != tg_id
            ]

            if not alive:
                await messages_kwargs.append({"text": _["dead_cant_vote"]})
            else:
                messages_kwargs.append(
                    {
                        "chat_id": f"{tg_id}",
                        "text": _["vote_instruction"],
                        "reply_markup": player_vote_ikm(other_players), 
                    }
                )
    else:
        messages_kwargs = [
            {"chat_id": f"{tg_id}", "text": message, "reply_markup": vote_rkm}
            for tg_id, name, alive, message in players_data
        ]
    for message_kwargs in messages_kwargs:
        await bot.send_message(**message_kwargs)


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
