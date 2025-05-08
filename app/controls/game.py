from asyncio import create_task, sleep

from flet import AlertDialog, Button, Container, Control, ControlEvent, Page, Row, Text

from ..misc import controls_of, get_game_players, post_game_start_voting


async def game(p: Page) -> tuple[Control, ...] | None:
    ps = p.session
    game_id = ps.get("game_id")
    if game_id is None:
        p.go("/")
        return

    round_text = Text(f"Раунд 1")
    players_text = Text("Игроки в игре")
    row = Row(
        [
            Container(Text(player["name"]))
            for player in await get_game_players(game_id)
            if player["alive"]
        ]
    )

    async def start_voting(_: ControlEvent):
        global task
        await post_game_start_voting(game_id)
        task = create_task(wait_voting_end())

    async def wait_voting_end():
        global task

        async def names() -> set[str]:
            return {
                player["name"]
                for player in await get_game_players(game_id)
                if player["alive"]
            }

        button.visible = False
        old_alive = await names()
        while True:
            await sleep(3)
            if kicked_player_set := (old_alive - (now_alive := await names())):
                kicked_player = kicked_player_set.pop()
                controls = controls_of(p)
                controls[2].controls = [Container(Text(name)) for name in now_alive]
                controls.append(
                    AlertDialog(
                        title=Text(f"Игрок {kicked_player} удален голосованием!")
                    )
                )
                await sleep(2.5)
                controls.pop()
                controls[0].value = f"Раунд {len(now_alive)}"
                button.visible = True
                task.cancel()

    button = Button("Начать голосование", on_click=start_voting)
    return (
        round_text,
        players_text,
        row,
        button,
    )
