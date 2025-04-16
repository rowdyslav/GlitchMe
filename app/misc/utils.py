from flet import Page


def get_view_controls(p: Page):
    return p.views[-1].controls[0].content.controls  # type: ignore
