from flet import Button, Control


async def game() -> tuple[Control, ...]:
    button = Button("Начать голосование")
    return (button,)
