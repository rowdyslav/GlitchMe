from aiohttp import ClientSession

from env import API_URL


async def post_create_game(rounds_count: int) -> bytes:
    async with ClientSession() as session:
        async with session.post(
            f"{API_URL}/game/create", params={"rounds_count": rounds_count}
        ) as response:
            return await response.content.read()
