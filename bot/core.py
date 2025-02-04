from aiogram import Bot
from environs import Env

env = Env()
env.read_env()

bot = Bot(token=env.str("BOT_TOKEN"))
