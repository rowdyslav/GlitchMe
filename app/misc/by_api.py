from aiohttp import ClientSession
from beanie import PydanticObjectId

from env import API_URL


async def post_game_create(rounds_count: int) -> tuple[bytes, str, int]:
    """
    Создать игру.
    Возвращает:
    - qr_bytes: QR-код для подключения
    - game_id: ID созданной игры
    - game_players_min_count: минимальное число игроков для старта
    """
    url = f"{API_URL}/game/create"
    params = {"rounds_count": rounds_count}
    async with ClientSession() as session:
        async with session.post(url, params=params) as resp:
            resp.raise_for_status()
            qr_bytes = await resp.read()
            headers = resp.headers
            return (
                qr_bytes,
                headers.get("game_id", ""),
                int(headers.get("game_players_min_count", 0)),
            )


async def post_game_start(game_id: PydanticObjectId) -> dict:
    """
    Запустить игру
    """
    url = f"{API_URL}/game/start/{game_id}"
    async with ClientSession() as session:
        async with session.post(url) as resp:
            resp.raise_for_status()
            return await resp.json()


async def get_game_players(game_id: PydanticObjectId) -> tuple[list[dict], bool]:
    """
    Получить список игроков и статус игры.
    Возвращает:
    - список dict (игроков)
    - флаг game_ended (завершена ли игра)
    """
    url = f"{API_URL}/game/players/{game_id}"
    async with ClientSession() as session:
        async with session.get(url) as resp:
            resp.raise_for_status()
            data = await resp.json()
            ended = resp.headers.get("game_ended") is not None
            return data, ended


async def post_game_start_voting(game_id: PydanticObjectId) -> dict:
    """
    Начать голосование
    """
    url = f"{API_URL}/game/start_voting/{game_id}"
    async with ClientSession() as session:
        async with session.post(url) as resp:
            resp.raise_for_status()
            return await resp.json()
