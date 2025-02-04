from aiogram import Router
from aiogram.utils.deep_linking import decode_payload
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message
from aiogram.utils.deep_linking import create_start_link
from bot import bot
from ..app.config import API_URL
from aiohttp import ClientSession
router = Router()



async def create_link(game_id):
    """Принимает id игры, возвращает ссылку для вступления"""
    link = await create_start_link(bot, game_id, encode=True)
    return link

@router.message(CommandStart(deep_link=True))
async def handler(message: Message, command: CommandObject):
    args = command.args
    game_id = decode_payload(args)
    player_id = message.from_user.id

    url = f"https://{API_URL}/games/connect/{game_id}/{player_id}"
    payload = {"game_id": game_id, "player_id": player_id}
    async with ClientSession() as session:
        async with session.post(url, json=payload, ssl=False) as response:
            data = await response.json()
            return data
        
    await message.answer(f"Your payload: {payload}")

# функция которая должна отправлять роли игроку
# лежит мёртвым грузом т.к. не понял как работать с webhook`ами
async def send_role(message: Message, chat_id, message_text):
    await bot.send_message(chat_id=chat_id, text=message_text)