from flet import Button, Container, Control, ControlEvent, Page, Row, Text

from ..misc import get_game_players, post_game_start_voting


async def game(p: Page) -> tuple[Control, ...] | None:
    ps = p.session
    game_id = ps.get("game_id")
    if game_id is None:
        p.go("/")
        return

    text = Text("Игроки в игре")
    row = Row(
        [
            Container(Text(player["name"]))
            for player in await get_game_players(game_id)
            if player["alive"]
        ]
    )

    async def start_voting(_: ControlEvent):
        await post_game_start_voting(game_id)
        p.go("/game")

    button = Button("Начать голосование", on_click=start_voting)
    return (
        text,
        row,
        button,
    )
