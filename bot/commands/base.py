from aiogram import Router
from aiogram.utils.deep_linking import decode_payload
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message
from aiogram.utils.deep_linking import create_start_link
from create_bot import main_bot
from misc import api
router = Router()
API_URL: str = "http://127.0.0.1:8000"


async def create_link(game_id):
    """Принимает id игры, возвращает ссылку для вступления"""
    link = await create_start_link(main_bot, game_id, encode=True)
    return link


@router.message(CommandStart(deep_link=True))
async def start_with_arg(message: Message, command: CommandObject):
    args = command.args
    game_id = decode_payload(args)
    player_id = message.from_user.id
    await api.connect_player(game_id=game_id, player_id=player_id)
    await message.answer(f"Your payload: {game_id}, {player_id}")


# заглушка если /start не без аргумента в ссылке
@router.message(CommandStart())
async def start_no_arg(message: Message):
    player_id = message.from_user.id
    game_id = "1"
    await api.connect_player(game_id=game_id, player_id=player_id)
    await message.answer(f"Your payload: {game_id}, {player_id}\n{1}")


# функция которая должна отправлять роли игроку
# лежит мёртвым грузом т.к. не понял как работать с webhook`ами
async def send_role(chat_id, message_text):
    await main_bot.send_message(chat_id=chat_id, text=message_text)
