from aiohttp import ClientSession
from flet import ControlEvent, Slider

from env import API_URL


async def post_create_game_wrapper(slider: Slider):
    async def post_create_game(_: ControlEvent) -> None:
        async with ClientSession() as session:
            async with session.post(
                f"{API_URL}/game/create", params={"rounds_count": slider.value}
            ) as response:
                return None

    return post_create_game
