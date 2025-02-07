from aiohttp import ClientSession
from beanie import PydanticObjectId
from config import API_URL


async def connect_player(game_id: PydanticObjectId, player_id: int) -> dict:
    async with ClientSession() as session:
        async with session.post(
            f"{API_URL}/games/connect/{game_id}",
            params={"player_id": player_id},
            ssl=False,
        ) as response:
            return await response.json()
