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

from ..misc import controls_of, get_game_players, post_game_start


async def lobby(p: Page) -> tuple[Text, Image, Text, Column] | None:
    ps = p.session

    qr_b64 = ps.get("qr_b64")
    game_id = ps.get("game_id")
    game_players_min_count = ps.get("game_players_min_count")
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

    async def start(_: ControlEvent):
        await post_game_start(game_id)
        p.go("/game")

    async def change_players_list() -> None:
        while True:
            await sleep(3)
            player_names = [
                player["name"] for player in await get_game_players(game_id)
            ]
            players_count = len(player_names)

            controls = controls_of(p)
            controls[2].value = f"Игроки {players_count}/{game_players_min_count}"
            controls[3].controls = [
                Text(
                    player_name,
                    text_align=TextAlign.START,
                    theme_style=TextThemeStyle.DISPLAY_MEDIUM,
                )
                for player_name in player_names
            ]

            if players_count >= game_players_min_count and len(controls) > 3:
                task.cancel()
                controls[0].value = controls[2].value
                controls[1] = controls[3]
                del controls[2:]
                controls.append(Button("Старт!", on_click=start))

            p.update()

    task = create_task(change_players_list())
    return (qr_text, qr_image, players_text, players_column)
