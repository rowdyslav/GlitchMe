from asyncio import create_task, sleep

from flet import (
    Button,
    Column,
    Control,
    ControlEvent,
    CrossAxisAlignment,
    Image,
    Page,
    Text,
    TextAlign,
    TextThemeStyle,
)

from ..misc import get_game_players, get_view_controls, post_game_start


async def lobby(p: Page) -> tuple[Control, ...] | None:
    qr_b64 = p.session.get("qr_b64")
    game_id = p.session.get("game_id")
    game_players_min_count = p.session.get("game_players_min_count")
    if qr_b64 is None or game_id is None or game_players_min_count is None:
        p.go("/")
        return

    qr_text = Text(
        "Отсканируй для подключения к игре!", theme_style=TextThemeStyle.DISPLAY_LARGE
    )
    qr_image = Image(src_base64=qr_b64)
    players_text = Text(
        f"Игроки 0/{game_players_min_count}",
        theme_style=TextThemeStyle.DISPLAY_LARGE,
    )
    players_column = Column(
        [],
        horizontal_alignment=CrossAxisAlignment.CENTER,
    )

    async def start_game(_: ControlEvent):
        await post_game_start(game_id)
        p.go("/game")

    async def change_players_list():
        player_names = [player["name"] for player in await get_game_players(game_id)]
        players_count = len(player_names)

        controls = get_view_controls(p)
        controls[2].value = f"Игроки {players_count}/{game_players_min_count}"
        controls[3].controls = [
            Text(
                player_name,
                text_align=TextAlign.START,
                theme_style=TextThemeStyle.DISPLAY_MEDIUM,
            )
            for player_name in player_names
        ]

        if players_count >= int(game_players_min_count) and len(controls > 3):
            task.cancel()
            controls[0].value = controls[2].value
            controls[1] = controls[3]
            del controls[2:]
            controls.append(Button("Старт!", on_click=start_game))

        p.update()

    async def t():
        while 1:
            await sleep(3)
            await change_players_list()

    task = create_task(t())
    return (qr_text, qr_image, players_text, players_column)
