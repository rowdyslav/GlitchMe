import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.utils.deep_linking import create_start_link
from beanie import PydanticObjectId
from fastapi import FastAPI
from pydantic import AnyUrl
from uvicorn import Config, Server

from env import BOT_TOKEN

from .commands import all_routers
from .misc import MAIN as _
from .misc import player_vote_ikm

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
webhook = FastAPI()


@webhook.get("/game_connect_link", response_model=AnyUrl)
async def game_connect_link(game_id: PydanticObjectId) -> AnyUrl:
    """Возвращает ссылку для подключения к игре"""

    return AnyUrl(await create_start_link(bot, str(game_id), encode=True))


@webhook.post("/send_messages/")
async def send_messages(
    players_data: list[tuple[str, int, bool]] | list[tuple[int, str, None]],
):
    """Отправляет сообщения в чаты
    tuple[name, tg_id, alive] | tuple[tg_id, message, _]"""

    no_messages = all([player[2] is not None for player in players_data])
    if no_messages:
        messages_kwargs: list[dict] = []
        for tg_id in map(lambda x: x[1], players_data):
            other_players = [
                {"name": player[0], "tg_id": player[1], "alive": player[2]}
                for player in players_data
                if player[1] != tg_id
            ]

            messages_kwargs.append(
                {
                    "chat_id": tg_id,
                    "text": _["vote_instruction"],
                    "reply_markup": player_vote_ikm(other_players),
                }
            )

    else:
        messages_kwargs = [
            {"chat_id": f"{tg_id}", "text": message}
            for tg_id, message, _ in players_data
        ]

    for m_kwargs in messages_kwargs:
        await bot.send_message(**m_kwargs)


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
