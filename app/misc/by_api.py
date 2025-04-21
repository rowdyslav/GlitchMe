from aiohttp import ClientSession
from beanie import PydanticObjectId

from env import API_URL


async def post_game_create(rounds_count: int) -> tuple[bytes, str, int]:
    async with ClientSession() as session:
        async with session.post(
            f"{API_URL}/game/create", params={"rounds_count": rounds_count}
        ) as response:
            return (
                await response.content.read(),
                response.headers["game_id"],
                int(response.headers["game_players_min_count"]),
            )


async def post_game_start(game_id: PydanticObjectId) -> None:
    async with ClientSession() as session:
        async with session.post(f"{API_URL}/game/start/{game_id}"):
            return


async def get_game_players(game_id: str) -> list[dict]:
    async with ClientSession() as session:
        async with session.get(f"{API_URL}/game/players/{game_id}") as response:
            return await response.json()
