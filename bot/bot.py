from aiogram import Bot
from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)