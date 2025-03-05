import asyncio

from aiohttp import ClientSession
from flet import (
    AppBar,
    AppView,
    Colors,
    CrossAxisAlignment,
    MainAxisAlignment,
    Page,
    RouteChangeEvent,
    Text,
    TextThemeStyle,
    Theme,
    View,
    ViewPopEvent,
    VisualDensity,
    app_async,
)
from flet.core.control_event import ControlEvent

from .src import home

TITLE = "GlitchMe!"
FONT = ("RubikWetPaint-Regular", "rubikwetpaint", "ofl")


async def main(page: Page):
    pv = page.views

    page.title = TITLE
    page.bgcolor = Colors.with_opacity(0.1, Colors.WHITE)
    page.fonts = {
        FONT[0]: "https://raw.githubusercontent.com/google/fonts/master/"
        f"{FONT[2]}/{FONT[1]}/{FONT[0]}.ttf",
    }
    page.theme = Theme(
        Colors.PURPLE_ACCENT_700,
        font_family=FONT[0],
        visual_density=VisualDensity.ADAPTIVE_PLATFORM_DENSITY,
    )

    async def route_change(_: RouteChangeEvent | ControlEvent):
        pv.clear()
        pv.append(
            View(
                "/",
                await home(),
                AppBar(
                    title=Text(
                        TITLE,
                        theme_style=TextThemeStyle.DISPLAY_LARGE,
                        scale=1.15,
                    ),
                    center_title=True,
                ),
                vertical_alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
            )
        )
        page.update()

    async def view_pop(_: ViewPopEvent):
        pv.pop()
        tvr = pv[-1].route
        assert tvr is not None
        page.go(tvr)

    page.on_route_change = route_change
    page.on_connect = route_change
    page.on_view_pop = view_pop

    page.go(page.route)


if __name__ == "__main__":
    asyncio.run(app_async(main, port=80, view=AppView.WEB_BROWSER))
