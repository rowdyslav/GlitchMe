from aiohttp import ClientSession
from beanie import PydanticObjectId
from environs import Env

env = Env()
env.read_env()

BOT_WEBHOOK_URL = env.str("BOT_WEBHOOK_URL")


async def get_game_link(game_id: PydanticObjectId) -> str:
    async with ClientSession() as session:
        async with session.get(
            f"{BOT_WEBHOOK_URL}/game_connect_link", params={"game_id": str(game_id)}
        ) as response:
            return await response.text()
