from flet import ControlEvent, TextField
from websockets.asyncio.client import connect


async def test_wrapper(text_field: TextField):
    async def test(_: ControlEvent):
        async with connect(
            "ws://127.0.0.1:8000/ws/67bf4166d3e0e1c3ff63a783"
        ) as websocket:
            assert (message := text_field.value) is not None
            await websocket.send(message)
            answer = await websocket.recv()
            print(answer)

    return test
