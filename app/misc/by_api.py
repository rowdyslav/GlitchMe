from aiohttp import ClientSession
from beanie import PydanticObjectId

from env import API_URL


async def post_game_create(rounds_count: int) -> tuple[bytes, str, int]:
    """Обращается к апи, создает игры. Возвращает биты qr-кода, id созданной игры и минимальное количество игроков для старта"""

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
        async with session.post(f"{API_URL}/game/start/{game_id}") as response:
            return await response.json()


async def get_game_players(game_id: PydanticObjectId) -> list[dict]:
    async with ClientSession() as session:
        async with session.get(f"{API_URL}/game/players/{game_id}") as response:
            return await response.json()


async def post_game_start_voting(game_id: PydanticObjectId):
    async with ClientSession() as session:
        async with session.post(f"{API_URL}/game/start_voting/{game_id}") as response:
            return await response.json()
