from base64 import b64encode

from flet import (
    Button,
    Colors,
    Control,
    ControlEvent,
    Icons,
    ProgressRing,
    Slider,
    Text,
    TextThemeStyle,
)

from config import ROUNDS_MAX_COUNT as mrc

from ..misc import controls_of, post_game_create


async def index() -> tuple[Control, ...]:
    text = Text("Количество раундов", theme_style=TextThemeStyle.DISPLAY_LARGE)
    slider = Slider(mrc, "{value}", 1, mrc, mrc - 1)

    async def create_game(_: ControlEvent) -> None:
        assert (p := slider.page) is not None

        controls = controls_of(p)
        del controls[2]
        controls[0].value = "Генерация QR-кода.."
        controls[1] = ProgressRing()
        p.update()

        qr_b64, game_id, game_players_min_count = await post_game_create(
            int(slider.value)
        )
        p.session.set(
            "qr_b64",
            b64encode(qr_b64).decode("ascii"),
        )
        p.session.set("game_id", game_id)
        p.session.set("game_players_min_count", game_players_min_count)

        p.go("/lobby")

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
