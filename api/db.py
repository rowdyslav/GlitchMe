from contextlib import asynccontextmanager

from beanie import init_beanie
from dns import resolver
from environs import Env
from fastapi import FastAPI
from icecream import ic
from motor.motor_asyncio import AsyncIOMotorClient
from schemas import Game

env = Env()
env.read_env()

resolver.default_resolver = resolver.Resolver(configure=False)
resolver.default_resolver.nameservers = ["8.8.8.8"]
client = AsyncIOMotorClient(env.str("API_MONGO_URL"))
db = client["GlitchMe"]


@asynccontextmanager
async def db_lifespan(_: FastAPI):
    ping_response = await db.command("ping")
    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")
    else:
        ic("Connected to database cluster.")
    await init_beanie(
        database=db,
        document_models=[
            Game,
        ],
    )
    yield
    client.close()
