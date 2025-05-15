from contextlib import asynccontextmanager

from beanie import init_beanie
from dns import resolver
from fastapi import FastAPI
from icecream import ic
from pymongo import AsyncMongoClient

from env import API_MONGO_URL

from .schemas import Game, Player

resolver.default_resolver = resolver.Resolver(configure=False)
resolver.default_resolver.nameservers = ["8.8.8.8"]
client = AsyncMongoClient(API_MONGO_URL)
db = client["GlitchMe"]


@asynccontextmanager
async def db_lifespan(_: FastAPI):
    ping_response = await db.command("ping")
    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")
    else:
        await init_beanie(
            database=db,  # type: ignore (Beanie еще не обновили до последнего Pymongo с асинк клиентом)
            document_models=[Game, Player],
        )
        ic("Connected to database cluster.")
    yield
    await client.close()
