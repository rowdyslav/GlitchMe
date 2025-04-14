from aiohttp import ClientSession
from beanie import PydanticObjectId

from env import API_URL


async def connect_player(game_id: PydanticObjectId, player_id: int, player_name: str):
    async with ClientSession() as session:
        await session.post(
            f"{API_URL}/game/connect/{game_id}",
            json={"name": player_name, "tg_id": player_id},
        )


async def get_players(game_id: PydanticObjectId) -> list | None:
    async with ClientSession() as session:
        async with session.get(f"{API_URL}/players/{game_id}") as resp:
            players = await resp.json() or None
            return players


async def player_inclusion(player_id: int):
    async with ClientSession() as session:
        await session.post(
            f"{API_URL}/game/inclusion/{player_id}",
        )
