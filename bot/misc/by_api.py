from aiohttp import ClientSession

from env import API_URL


async def patch_game_connect(game_id: str, player_tg_id: int, player_name: str) -> None:
    async with ClientSession() as session:
        await session.patch(
            f"{API_URL}/game/connect/{game_id}",
            json={"name": player_name, "tg_id": player_tg_id},
        )


async def get_game_players(game_id: str) -> list:
    async with ClientSession() as session:
        async with session.get(f"{API_URL}/game/players/{game_id}") as response:
            return await response.json()


async def patch_player_vote(player_tg_id: int, voted_tg_id: int) -> int:
    async with ClientSession() as session:
        async with session.patch(
            f"{API_URL}/player/vote/{player_tg_id}", params={"voted_tg_id": voted_tg_id}
        ) as response:
            return response.status
