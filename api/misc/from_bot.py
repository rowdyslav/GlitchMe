from aiohttp import ClientSession
from beanie import PydanticObjectId


async def get_game_link(game_id: PydanticObjectId):
    async with ClientSession() as session:
        async with session.get(
            "http://127.0.0.1:5000/get_link", params={"game_id": str(game_id)}
        ) as response:
            return await response.text()
