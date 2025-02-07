import asyncio

from aiohttp import ClientSession
from config import API_URL
from flet import (
    Button,
    CrossAxisAlignment,
    MainAxisAlignment,
    Page,
    RouteChangeEvent,
    Slider,
    Text,
    TextThemeStyle,
    View,
    ViewPopEvent,
    app_async,
)
from flet.core.control_event import ControlEvent


async def get_max_rounds_count():
    async with ClientSession() as session:
        return int(
            await (await session.get(f"{API_URL}/games/max_rounds_count/")).text()
        )


async def main(page: Page):
    page.title = "GlitchMe"

    text = Text("Количество раундов", theme_style=TextThemeStyle.DISPLAY_LARGE)
    slider = Slider(1, "{value}", 1, (m := await get_max_rounds_count()), m - 1)

    async def create_game(_: ControlEvent):
        async with ClientSession() as session:
            return await session.post(
                f"{API_URL}/games/create", params={"rounds_count": slider.value}
            )

    button = Button(
        "Создать игру",
        "GAMEPAD",
        "#ffffff",
        "GREEN",
        "#000000",
        on_click=create_game,
        autofocus=True,
        scale=2,
    )

    async def route_change(_: RouteChangeEvent | ControlEvent):
        page.views.clear()
        page.views.append(
            View(
                controls=[text, slider, button],
                vertical_alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
            )
        )
        page.update()

    async def view_pop(_: ViewPopEvent):
        page.views.pop()
        top_view = page.views[-1]
        assert top_view.route
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_connect = route_change
    page.on_view_pop = view_pop

    page.go(page.route)


asyncio.run(app_async(main))
