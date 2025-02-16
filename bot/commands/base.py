from aiogram import F, Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import Message
from aiogram.utils.deep_linking import decode_payload
from beanie import PydanticObjectId
from misc.by_api import connect_player

router = Router()


@router.message(CommandStart(deep_link=True, magic=F.args))
async def start(message: Message, command: CommandObject):
    args = command.args
    assert args is not None
    game_id = PydanticObjectId(decode_payload(args))
    assert (user := message.from_user) is not None
    player_id = user.id
    player_name = user.username or f"{user.first_name}ⁿⁿ"
    await connect_player(game_id, player_id, player_name)
    await message.answer(f"{player_name}, вы успешно подключились к игре {game_id}!")
