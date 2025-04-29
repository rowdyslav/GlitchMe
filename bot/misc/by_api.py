from aiohttp import ClientSession
from beanie import PydanticObjectId

from env import API_URL


async def post_game_connect(
    game_id: PydanticObjectId, player_tg_id: int, player_name: str
) -> None:
    async with ClientSession() as session:
        await session.post(
            f"{API_URL}/game/connect/{game_id}",
            json={"name": player_name, "tg_id": player_tg_id},
        )


async def get_game_players(game_id: PydanticObjectId) -> list | None:
    async with ClientSession() as session:
        async with session.get(f"{API_URL}/game/players/{game_id}") as resp:
            return await resp.json() or None


async def post_player_vote(player_tg_id: int) -> None:
    async with ClientSession() as session:
        await session.post(
            f"{API_URL}/player/vote/{player_tg_id}",
        )
