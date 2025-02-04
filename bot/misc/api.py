from aiohttp import ClientSession

API_URL: str = "http://127.0.0.1:8000"


async def connect_player(game_id, player_id):
    url = f"{API_URL}/games/connect/{game_id}/{player_id}"
    async with ClientSession() as session:
        async with session.post(url, ssl=False) as response:
            data = await response.json()
            return data
