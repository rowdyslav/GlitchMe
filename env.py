from environs import Env

env = Env()
env.read_env()

API_URL = env.str("API_URL")
API_MONGO_URL = env.str("API_MONGO_URL")

BOT_TOKEN = env.str("BOT_TOKEN")
BOT_WEBHOOK_URL = env.str("BOT_WEBHOOK_URL")
