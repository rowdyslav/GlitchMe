from flet import (
    AppBar,
    AppView,
    Colors,
    Column,
    ControlEvent,
    CrossAxisAlignment,
    MainAxisAlignment,
    Page,
    RouteChangeEvent,
    SelectionArea,
    Text,
    TextThemeStyle,
    Theme,
    View,
    ViewPopEvent,
    VisualDensity,
    app_async,
)

from .controls import game, index, lobby

TITLE = "GlitchMe!"
FONT_FOLDER = "ofl"
FONT_KEY = "rubikwetpaint"
FONT_NAME = "RubikWetPaint-Regular"
FONT_PATH = (
    "https://raw.githubusercontent.com/google/fonts/master/"
    f"{FONT_FOLDER}/{FONT_KEY}/{FONT_NAME}.ttf"
)

SCREENS = {
    "/": index,
    "/lobby": lobby,
    "/game": game,
}


async def main(p: Page):
    p.bgcolor = Colors.with_opacity(0.1, Colors.WHITE)
    p.fonts = {FONT_NAME: FONT_PATH}
    p.theme = Theme(
        Colors.PURPLE_ACCENT_700,
        font_family=FONT_NAME,
        visual_density=VisualDensity.ADAPTIVE_PLATFORM_DENSITY,
    )

    pvs = p.views

    async def on_route_change(_: RouteChangeEvent | ControlEvent):
        setup_screen = SCREENS.get(p.route, index)
        view = View(
            controls=(
                SelectionArea(
                    Column(
                        await setup_screen(p),
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        spacing=25,
                        expand=True,
                    )
                ),
            ),
            appbar=AppBar(
                title=Text(TITLE, theme_style=TextThemeStyle.DISPLAY_LARGE),
                center_title=True,
            ),
            horizontal_alignment=CrossAxisAlignment.CENTER,
            vertical_alignment=MainAxisAlignment.CENTER,
        )
        pvs.clear()
        pvs.append(view)
        p.update()

    async def on_view_pop(_: ViewPopEvent):
        if len(pvs) > 1:
            pvs.pop()
            p.go(pvs[-1].route or "/")

    p.on_route_change = on_route_change
    p.on_connect = on_route_change
    p.on_view_pop = on_view_pop

    p.go(p.route)


if __name__ == "__main__":
    from asyncio import run

    run(app_async(main, port=80, view=AppView.WEB_BROWSER))
