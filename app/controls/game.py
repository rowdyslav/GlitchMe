from flet import Button, Control


async def game() -> tuple[Control, ...]:
    button = Button("Следующий раунд")
    return (button,)
