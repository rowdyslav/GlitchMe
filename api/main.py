from collections import defaultdict

from db import db_lifespan
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic_core import ValidationError
from routers.games import router

app = FastAPI(lifespan=db_lifespan)


@app.exception_handler(ValidationError)
async def handler(_: Request, exc: ValidationError):
    reformatted_message = defaultdict(list)
    for error in exc.errors():
        loc, msg = tuple(map(str, error["loc"])), error["msg"]
        filtered_loc = loc[1:] if loc[0] in ("body", "query", "path") else loc
        reformatted_message[".".join(filtered_loc)].append(msg)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {"detail": "Bad request", "errors": reformatted_message}
        ),
    )


app.include_router(router)
