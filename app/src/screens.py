from flet import Button, Colors, Control, Icons, Slider, Text, TextThemeStyle

from .from_api import get_create_game_func, get_max_rounds_count


async def home() -> tuple[Control, ...]:
    text = Text(
        "Количество раундов",
        theme_style=TextThemeStyle.DISPLAY_LARGE,
    )
    slider = Slider(
        m := await get_max_rounds_count(),
        "{value}",
        1,
        m,
        m - 1,
    )
    button = Button(
        "Создать игру",
        Icons.GAMEPAD,
        Colors.WHITE,
        Colors.GREEN,
        Colors.TRANSPARENT,
        on_click=await get_create_game_func(slider),
        scale=2,
    )

    return (text, slider, button)
