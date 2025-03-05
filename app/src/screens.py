from aiohttp import ClientSession
from beanie import PydanticObjectId
from flet import Button, Colors, Control, Icons, Slider, Text, TextField, TextThemeStyle

from config import MAX_ROUNDS_COUNT as mrc

from ..misc.by_ws import test_wrapper
from ..misc.from_api import post_create_game_wrapper


async def home() -> tuple[Control, ...]:
    text = Text("Количество раундов", theme_style=TextThemeStyle.DISPLAY_LARGE)
    slider = Slider(mrc, "{value}", 1, mrc, mrc - 1)
    button = Button(
        "Создать игру",
        Icons.GAMEPAD,
        Colors.WHITE,
        Colors.GREEN,
        Colors.TRANSPARENT,
        on_click=await post_create_game_wrapper(slider),
        scale=2,
    )
    text_field = TextField()

    ws_button = Button("Тест сокета", on_click=await test_wrapper(text_field))
    return (text, slider, button, text_field, ws_button)
