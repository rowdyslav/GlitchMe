from contextlib import asynccontextmanager

from beanie import init_beanie
from dns.resolver import Resolver, default_resolver
from fastapi import FastAPI
from icecream import ic
from motor.motor_asyncio import AsyncIOMotorClient

from env import API_MONGO_URL

from .schemas import Game, Player

default_resolver = Resolver(configure=False)
default_resolver.nameservers = ["8.8.8.8"]
client = AsyncIOMotorClient(API_MONGO_URL)
db = client["GlitchMe"]


@asynccontextmanager
async def db_lifespan(_: FastAPI):
    ping_response = await db.command("ping")
    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")
    else:
        await init_beanie(
            database=db,
            document_models=[Game, Player],
        )
        ic("Connected to database cluster.")
    yield
    client.close()
