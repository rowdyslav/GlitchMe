from flet import Button, Colors, Control, Icons, Slider, Text, TextThemeStyle

from config import MAX_ROUNDS_COUNT as mrc

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
    return (text, slider, button)
