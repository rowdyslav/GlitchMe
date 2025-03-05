from aiohttp import ClientSession, ClientWebSocketResponse, WSMsgType
from flet import ControlEvent, TextField


async def test_wrapper(text_field: TextField):
    from icecream import ic

    ic()

    async def test(_: ControlEvent):
        assert (text := text_field.value) is not None
        ic()
        async with ClientSession() as session:
            async with session.ws_connect(
                "ws://127.0.0.1:8000/ws/control/67bf4166d3e0e1c3ff63a783",
                autoclose=False,
                autoping=False,
            ) as ws:
                ic(1)
                await ws.send_str(text)
                ic(2)
                async for msg in ws:
                    ic(12)
                    if msg.type == WSMsgType.TEXT:
                        print(f"SERVER says - {msg.data}")
                    elif msg.type == WSMsgType.ERROR:
                        break
                    else:
                        print("хз")

    return test
