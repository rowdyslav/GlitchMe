from aiohttp import ClientSession
from beanie import PydanticObjectId
from pydantic import AnyUrl

from env import BOT_WEBHOOK_URL


async def get_game_connect_link(game_id: PydanticObjectId) -> AnyUrl:
    async with ClientSession() as session:
        async with session.get(
            f"{BOT_WEBHOOK_URL}/game_connect_link", params={"game_id": str(game_id)}
        ) as response:
            return AnyUrl((await response.text()).strip('"'))
