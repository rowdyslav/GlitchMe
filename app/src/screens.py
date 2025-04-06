from base64 import b64encode

from flet import (
    Button,
    Colors,
    Control,
    Icons,
    Image,
    Page,
    ProgressRing,
    Slider,
    Text,
    TextThemeStyle,
)
from flet.core.control_event import ControlEvent

from config import MAX_ROUNDS_COUNT as mrc

from .by_api import post_create_game


async def home() -> tuple[Control, ...]:
    text = Text("Количество раундов", theme_style=TextThemeStyle.DISPLAY_LARGE)
    slider = Slider(mrc, "{value}", 1, mrc, mrc - 1)

    async def create_game(_: ControlEvent) -> None:
        assert (p := slider.page) is not None
        controls = p.views[-1].controls[0].content.controls  # type: ignore
        del controls[2]
        controls[0].value = "Генерация QR-кода.."
        controls[1] = ProgressRing()
        p.update()
        p.session.set(
            "qr_b64",
            b64encode(await post_create_game(int(slider.value))).decode("ascii"),
        )
        p.go("/game")

    button = Button(
        "Создать игру",
        Icons.GAMEPAD,
        Colors.WHITE,
        Colors.GREEN,
        Colors.TRANSPARENT,
        on_click=create_game,
        scale=2,
    )
    return (text, slider, button)


async def game(p: Page) -> tuple[Control, ...] | None:
    qr_b64 = p.session.get("qr_b64")
    if qr_b64 is None:
        p.go("/")
        return
    text = Text(
        "Отсканируй для подключения к игре!", theme_style=TextThemeStyle.DISPLAY_LARGE
    )
    qr = Image(src_base64=qr_b64)
    return (
        text,
        qr,
    )
