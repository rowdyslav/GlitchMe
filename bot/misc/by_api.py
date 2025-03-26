from aiohttp import ClientSession
from beanie import PydanticObjectId

from env import API_URL


async def connect_player(game_id: PydanticObjectId, player_id: int, player_name: str):
    async with ClientSession() as session:
        await session.post(
            f"{API_URL}/game/connect/{game_id}",
            json={"name": player_name, "tg_id": player_id},
        )


async def get_game(game_id: id) -> dict | None:
    async with ClientSession() as session:
        async with session.get(f"{API_URL}/players/{game_id}") as resp:
            players = await resp.json() or None
            return players
