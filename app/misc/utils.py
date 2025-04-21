from flet import Page


def controls_of(p: Page) -> list:
    """Возвращает массив виджетов из последнего вью структуры View(SelectionArea(Column([...])))"""

    return p.views[-1].controls[0].content.controls  # type: ignore
