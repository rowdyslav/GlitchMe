from aiohttp.client_exceptions import ClientConnectorError
from db import db_lifespan
from fastapi import FastAPI
from misc import bad_request, client_connection
from pydantic_core import ValidationError
from routers import all_routers

app = FastAPI(lifespan=db_lifespan)
app.add_exception_handler(ValidationError, bad_request)
app.add_exception_handler(ClientConnectorError, client_connection)

for router in all_routers:
    app.include_router(router)
