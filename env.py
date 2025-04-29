from environs import Env

env = Env()
env.read_env()

APP_URL = env.str("APP_URL")

API_URL = env.str("API_URL")
API_MONGO_URL = env.str("API_MONGO_URL")

BOT_TOKEN = env.str("BOT_TOKEN")
BOT_WEBHOOK_URL = env.str("BOT_WEBHOOK_URL")
