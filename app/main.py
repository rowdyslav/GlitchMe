import asyncio

from base.screens import home
from flet import (
    AppView,
    CrossAxisAlignment,
    MainAxisAlignment,
    Page,
    RouteChangeEvent,
    View,
    ViewPopEvent,
    app_async,
)
from flet.core.control_event import ControlEvent
from flet_restyle import FletReStyle, FletReStyleConfig, google_font


async def main(page: Page):
    page.title = "GlitchMe!"

    async def route_change(_: RouteChangeEvent | ControlEvent):
        page.views.clear()
        page.views.append(
            View(
                controls=await home(),
                vertical_alignment=MainAxisAlignment.CENTER,
                horizontal_alignment=CrossAxisAlignment.CENTER,
            )
        )
        page.update()

    async def view_pop(_: ViewPopEvent):
        page.views.pop()
        top_view = page.views[-1]
        assert top_view.route
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_connect = route_change
    page.on_view_pop = view_pop

    font = "RubikWetPaint-Regular"
    FletReStyleConfig.theme.font_family = font
    FletReStyleConfig.font = (
        font,
        f"https://raw.githubusercontent.com/google/fonts/master/ofl/rubikwetpaint/{font}.ttf",
    )
    FletReStyle.apply_config(page, FletReStyleConfig())
    page.go(page.route)


asyncio.run(app_async(main, view=AppView.WEB_BROWSER))
