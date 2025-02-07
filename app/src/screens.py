from flet import AppBar, Button, Control, Slider, Text, TextThemeStyle

from .from_api import get_create_game_func, get_max_rounds_count


async def home() -> tuple[Control, ...]:
    appbar = AppBar(
        title=Text("GlitchMe!", theme_style=TextThemeStyle.DISPLAY_LARGE, scale=1.15),
        center_title=True,
    )
    text = Text("Количество раундов", theme_style=TextThemeStyle.DISPLAY_LARGE)
    slider = Slider(m := await get_max_rounds_count(), "{value}", 1, m, m - 1)
    button = Button(
        "Создать игру",
        "GAMEPAD",
        "#ffffff",
        "GREEN",
        "#000000",
        on_click=await get_create_game_func(slider),
        scale=2,
    )

    return (appbar, text, slider, button)
