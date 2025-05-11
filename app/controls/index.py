from base64 import b64encode

from flet import (
    Button,
    ControlEvent,
    MainAxisAlignment,
    Page,
    ProgressRing,
    Row,
    Slider,
    Text,
    icons,
)

from config import ROUNDS_MAX_COUNT as mrc

from ..misc import post_game_create


async def index(p: Page):
    text = Text("Количество раундов", size=24)
    slider = Slider(min=1, max=mrc, value=mrc - 1, label="{value}", divisions=mrc - 1)

    async def create(_: ControlEvent):
        slider.disabled = True
        button.disabled = True
        progress_ring.visible = True
        p.update()
        qr_b64, game_id, game_players_min_count = await post_game_create(
            int(slider.value)
        )
        ps = p.session
        ps.set(
            "qr_b64",
            b64encode(qr_b64).decode("ascii"),
        )
        ps.set("game_id", game_id)
        ps.set("game_players_min_count", game_players_min_count)
        p.go("/lobby")

    row = Row(
        [
            button := Button(
                text="Создать игру",
                icon=icons.GAMEPAD,
                on_click=create,
                expand=True,
            ),
            progress_ring := ProgressRing(visible=False),
        ],
        alignment=MainAxisAlignment.CENTER,
    )

    return (text, slider, row)
