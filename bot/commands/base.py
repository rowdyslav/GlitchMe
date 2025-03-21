from aiogram import F, Router
from aiogram.filters import CommandObject, CommandStart, Command
from aiogram.types import Message
from aiogram.utils.deep_linking import decode_payload
from aiogram.enums.parse_mode import ParseMode
from beanie import PydanticObjectId
from bot.commands.command_texts import HELP_TEXT
from ..misc.by_api import connect_player, get_players

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


@router.message(CommandStart())
async def start_light(message: Message):
    assert (user := message.from_user) is not None
    player_name = user.username or f"{user.first_name}ⁿⁿ"
    await message.answer(f"Привет, {player_name}!\n/help - помощь")


@router.message(Command(commands=["help", "h", "description"]))
async def help_command(message: Message):
    await message.answer(HELP_TEXT, parse_mode=ParseMode.HTML)


# нужна ли функция? получение списка игроков
@router.message(Command("players"))
async def get_players_list(message: Message):
    players = get_players(message.from_user.id)
    pretty_players = "\n".join(list(players.values()))
    await message.answer(pretty_players)
