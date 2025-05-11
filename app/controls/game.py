from asyncio import create_task, sleep

from flet import (
    AlertDialog,
    Button,
    Column,
    ControlEvent,
    MainAxisAlignment,
    Page,
    Row,
    Text,
    TextAlign,
)

from ..misc import get_game_players, post_game_start_voting


async def game(p: Page) -> tuple[Text, Row, Button] | None:
    p.title += " Игра"

    game_id = p.session.get("game_id")
    if not game_id:
        p.go("/")
        return

    round_num = 1

    text = Text(f"Раунд {round_num}", size=24, text_align=TextAlign.CENTER)
    row = Row([], alignment=MainAxisAlignment.CENTER, spacing=10)

    async def get_alive_players_names():
        players, ended = await get_game_players(game_id)
        alive = {player["name"] for player in players if player["alive"]}
        return alive, ended

    def set_players_names(players_names: set[str]):
        row.controls = [Text(n, text_align=TextAlign.START) for n in players_names]
        p.update()

    alive_players_names = (await get_alive_players_names())[0]
    set_players_names(alive_players_names)

    async def monitor_voting():
        nonlocal round_num, alive_players_names

        old_alive = alive_players_names.copy()
        while True:
            await sleep(3)
            now_alive, ended = await get_alive_players_names()
            kicked = old_alive - now_alive
            if kicked:
                p.open(
                    AlertDialog(
                        title=Text(f"Игрок {kicked.pop()} исключен голосованием!")
                    )
                )
                if ended:
                    winners = [Text(n) for n in now_alive]
                    p.open(
                        AlertDialog(
                            title=Column(
                                [
                                    Text(
                                        f"Победил{"и игроки" if len(now_alive) > 1 else " Глюк"}",
                                        size=20,
                                    )
                                ]
                                + winners,
                                spacing=10,
                            )
                        )
                    )
                else:
                    round_num += 1
                    text.value = f"Раунд {round_num}"
                    set_players_names(now_alive)

                    button.visible = True
                    p.update()
                break

    async def start_voting(_: ControlEvent):
        button.visible = False
        p.update()

        await post_game_start_voting(game_id)
        create_task(monitor_voting())

    button = Button("Начать голосование", on_click=start_voting, expand=True)

    return (text, row, button)
