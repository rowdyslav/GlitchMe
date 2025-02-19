from aiohttp.client_exceptions import ClientConnectorError
from db import db_lifespan
from fastapi import FastAPI
from misc import client_connector, validation
from pydantic_core import ValidationError
from routers import all_routers

app = FastAPI(lifespan=db_lifespan)
app.add_exception_handler(ValidationError, validation)
app.add_exception_handler(ClientConnectorError, client_connector)

for router in all_routers:
    app.include_router(router)
