from flet import Button, Container, Control, Page, Row, Text

from ..misc import get_game_players


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
    button = Button("Начать голосование")
    return (
        text,
        row,
        button,
    )
