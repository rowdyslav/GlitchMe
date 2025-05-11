from asyncio import create_task, sleep

from flet import (
    Button,
    Column,
    ControlEvent,
    CrossAxisAlignment,
    Image,
    Page,
    Text,
    TextAlign,
    TextThemeStyle,
)

from ..misc import get_game_players, post_game_start


async def lobby(p: Page) -> tuple[Text, Image, Text, Column, Button] | None:
    p.title += " Лобби"
    ps = p.session

    qr_b64 = ps.get("qr_b64")
    game_id = ps.get("game_id")
    game_players_min_count = ps.get("game_players_min_count")
    if qr_b64 is None or game_id is None or game_players_min_count is None:
        p.go("/")
        return

    qr_text = Text(
        "Отсканируй для подключения к игре!",
        theme_style=TextThemeStyle.DISPLAY_LARGE,
        text_align=TextAlign.CENTER,
    )
    qr_image = Image(src_base64=qr_b64)

    players_text = Text(
        f"Игроки 0/{game_players_min_count}",
        theme_style=TextThemeStyle.DISPLAY_LARGE,
        text_align=TextAlign.CENTER,
    )
    players_column = Column(
        [],
        horizontal_alignment=CrossAxisAlignment.CENTER,
        spacing=5,
    )

    async def start(_: ControlEvent):
        await post_game_start(game_id)
        p.go("/game")

    start_button = Button(
        text="Старт!",
        on_click=start,
        disabled=True,
    )

    async def monitor_players():
        while True:
            await sleep(3)
            players = (await get_game_players(game_id))[0]
            names = [player["name"] for player in players]
            players_count = len(names)

            players_text.value = f"Игроки {players_count}/{game_players_min_count}"
            players_column.controls = [
                Text(
                    name,
                    text_align=TextAlign.START,
                    theme_style=TextThemeStyle.BODY_MEDIUM,
                )
                for name in names
            ]

            if players_count >= game_players_min_count:
                start_button.disabled = False
                break

            p.update()

    create_task(monitor_players())
    return (qr_text, qr_image, players_text, players_column, start_button)
