from asyncio import create_task, sleep

from flet import (
    AlertDialog,
    Button,
    Column,
    Control,
    ControlEvent,
    MainAxisAlignment,
    Page,
    Row,
    Text,
)

from ..misc import controls_of, get_game_players, post_game_start_voting


async def game(p: Page) -> tuple[Control, ...] | None:
    ps = p.session
    game_id = ps.get("game_id")
    if game_id is None:
        p.go("/")
        return

    round_text = Text(f"Раунд 1")
    players_text = Text("Игроки в игре")

    async def names() -> tuple[set[str], bool]:
        players, game_ended = await get_game_players(game_id)
        return (
            {player["name"] for player in players if player["alive"]},
            game_ended,
        )

    row = Row([Text(name) for name in (await names())[0]], MainAxisAlignment.CENTER)

    async def start_voting(_: ControlEvent):
        global task
        await post_game_start_voting(game_id)
        task = create_task(wait_voting_end())

    async def wait_voting_end():
        global task

        button.visible = False
        p.update()
        old_alive = (await names())[0]
        while True:
            await sleep(3)
            now_alive, game_ended = await names()
            if kicked_player_set := old_alive - now_alive:
                if game_ended:
                    p.open(
                        AlertDialog(
                            title=(
                                lambda x: Column(
                                    [
                                        Text(value)
                                        for value in now_alive.union({f"Победил{x}"})
                                    ]
                                )
                            )("и игроки" if len(now_alive) > 1 else " Глюк")
                        )
                    )
                else:
                    controls = controls_of(p)
                    controls[0].value = f"Раунд {len(now_alive)}"
                    controls[2].controls = [Text(name) for name in now_alive]
                    button.visible = True
                    p.update()
                p.open(
                    AlertDialog(
                        title=Text(
                            f"Игрок {kicked_player_set.pop()} удален голосованием!"
                        )
                    )
                )
                task.cancel()
                break

    button = Button("Начать голосование", on_click=start_voting)
    return (
        round_text,
        players_text,
        row,
        button,
    )
