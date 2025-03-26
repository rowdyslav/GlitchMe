from aiogram import F, Router
from aiogram.filters import CommandObject, CommandStart, Command
from aiogram.types import Message
from aiogram.utils.deep_linking import decode_payload
from aiogram.enums.parse_mode import ParseMode
from beanie import PydanticObjectId
from bot.commands.command_texts import HELP_TEXT
from ..misc.by_api import connect_player, get_game

router = Router()

players_game_ids = {}


@router.message(CommandStart(deep_link=True, magic=F.args))
async def start(message: Message, command: CommandObject):
    args = command.args
    assert args is not None
    game_id = PydanticObjectId(decode_payload(args))
    assert (user := message.from_user) is not None
    player_id = user.id
    player_name = user.username or f"{user.first_name}ⁿⁿ"
    await connect_player(game_id, player_id, player_name)
    players_game_ids[player_id] = game_id
    await message.answer(f"{player_name}, вы успешно подключились к игре {game_id}!")


@router.message(CommandStart())
async def start_light(message: Message):
    assert (user := message.from_user) is not None
    player_name = user.username or f"{user.first_name}ⁿⁿ"
    await message.answer(f"Привет, {player_name}!\n/help - помощь")


@router.message(Command(commands=["help", "h", "description"]))
async def help_command(message: Message):
    await message.answer(HELP_TEXT)


# нужна ли функция? получение списка игроков
@router.message(Command("players"))
async def players(message: Message):
    user_id = message.from_user.id
    if user_id not in players_game_ids:
        await message.answer("Вы не в игре!")
        return
    players = get_game(players_game_ids[user_id])
    # id : [name: str, alive: bool]
    pretty_players = "\n".join(
        [
            i["name"] if i["alive"] else f"<s>{i['name']}</s>"
            for i in list(players.values())
        ]
    )
    await message.answer(pretty_players)


@router.message(F.text)
async def wrong_query(message: Message):
    await message.answer("Простите, я вас не понимаю(")
