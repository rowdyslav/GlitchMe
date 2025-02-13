from collections import defaultdict

from aiohttp.client_exceptions import ClientConnectorError
from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic_core import ValidationError


async def bad_request(_: Request, exc: Exception):
    assert isinstance(exc, ValidationError)
    from icecream import ic

    ic(exc, exc.errors())
    related_errors: dict[str, list[str]] = defaultdict(list)
    for error in exc.errors():
        loc, msg = tuple(map(str, error["loc"])), error["msg"]
        filtered_loc = loc[1:] if loc and loc[0] in ("body", "query", "path") else loc
        related_errors[".".join(filtered_loc)].append(msg)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {"detail": "Bad request", "related_errors": related_errors}
        ),
    )


async def client_connection(_: Request, exc: Exception):
    assert isinstance(exc, ClientConnectorError)

    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content=jsonable_encoder(
            {"detail": "Ошибка подключения к стороннему или внутреннему API"}
        ),
    )
