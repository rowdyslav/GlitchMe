from aiohttp.client_exceptions import ClientConnectorError
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic_core import ValidationError

from .db import db_lifespan
from .misc import client_connector, validation
from .routers import all_routers

app = FastAPI(lifespan=db_lifespan)
app.add_exception_handler(ValidationError, validation)
app.add_exception_handler(ClientConnectorError, client_connector)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in all_routers:
    app.include_router(router)
