from aiohttp import ClientSession
from environs import Env
from flet import ControlEvent, Slider

env = Env()
env.read_env()

API_URL = env.str("API_URL")


async def get_max_rounds_count() -> int:
    async with ClientSession() as session:
        return int(
            await (await session.get(f"{API_URL}/game/max_rounds_count/")).text()
        )


async def get_create_game_func(slider: Slider):
    async def create_game(_: ControlEvent) -> None:
        async with ClientSession() as session:
            await session.post(
                f"{API_URL}/game/create", params={"rounds_count": slider.value}
            )

    return create_game
