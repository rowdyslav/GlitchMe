from typing import Dict

from aiohttp import ClientSession
from beanie import PydanticObjectId
from config import API_URL


async def connect_player(game_id: PydanticObjectId, player_id: int) -> Dict:
    url = f"{API_URL}/games/connect/{game_id}"
    async with ClientSession() as session:
        async with session.post(
            url, params={"player_id": player_id}, ssl=False
        ) as response:
            data = await response.json()
            return data
