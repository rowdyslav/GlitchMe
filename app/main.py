from flet import (
    AppBar,
    AppView,
    Colors,
    Column,
    CrossAxisAlignment,
    MainAxisAlignment,
    Page,
    RouteChangeEvent,
    SelectionArea,
    TemplateRoute,
    Text,
    TextThemeStyle,
    Theme,
    View,
    ViewPopEvent,
    VisualDensity,
    app_async,
)
from flet.core.control_event import ControlEvent

from .src import game, home

TITLE = "GlitchMe!"
FONT = ("RubikWetPaint-Regular", "rubikwetpaint", "ofl")


async def main(p: Page):
    pv = p.views

    p.title = TITLE
    p.bgcolor = Colors.with_opacity(0.1, Colors.WHITE)
    p.fonts = {
        FONT[0]: "https://raw.githubusercontent.com/google/fonts/master/"
        f"{FONT[2]}/{FONT[1]}/{FONT[0]}.ttf",
    }
    p.theme = Theme(
        Colors.PURPLE_ACCENT_700,
        font_family=FONT[0],
        visual_density=VisualDensity.ADAPTIVE_PLATFORM_DENSITY,
    )

    async def route_change(_: RouteChangeEvent | ControlEvent):
        pv.clear()
        troute = TemplateRoute(p.route)
        if troute.match("/game"):
            screen = await game(p)
        else:
            screen = await home()
        pv.append(
            View(
                "/",
                (
                    SelectionArea(
                        Column(
                            screen,
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                        )
                    ),
                ),
                AppBar(
                    title=Text(
                        TITLE,
                        theme_style=TextThemeStyle.DISPLAY_LARGE,
                        scale=1.15,
                    ),
                    center_title=True,
                ),
                horizontal_alignment=CrossAxisAlignment.CENTER,
                vertical_alignment=MainAxisAlignment.CENTER,
            )
        )
        p.update()

    async def view_pop(_: ViewPopEvent):
        pv.pop()
        tvr = pv[-1].route
        assert tvr is not None
        p.go(tvr)

    p.on_route_change = route_change
    p.on_connect = route_change
    p.on_view_pop = view_pop

    p.go(p.route)


if __name__ == "__main__":
    from asyncio import run

    run(app_async(main, port=80, view=AppView.WEB_BROWSER))
