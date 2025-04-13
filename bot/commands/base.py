from aiogram import F, Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import Message
from aiogram.utils.deep_linking import decode_payload
from aiogram.types import CallbackQuery
from beanie import PydanticObjectId
from bot.commands.command_texts import HELP_TEXT
from .keyboard import players_kb, PlayerCallback
from ..misc.by_api import connect_player, get_players

router = Router()

players_game_ids = {}


@router.message(CommandStart(deep_link=True, magic=F.args))
async def start_link(message: Message, command: CommandObject):
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
async def start(message: Message):
    assert (user := message.from_user) is not None
    player_name = user.username or f"{user.first_name}ⁿⁿ"
    await message.answer(f"Привет, {player_name}!\n/help - помощь")


@router.message(Command(commands=["help", "h", "description"]))
async def help_command(message: Message):
    await message.answer(HELP_TEXT)


@router.message(Command("players"))
async def players(message: Message):
    user_id = message.from_user.id
    if user_id not in players_game_ids:
        await message.answer("Вы не в игре!")
        return
    players = get_players(players_game_ids[user_id])
    # id : [name: str, alive: bool]
    pretty_players = "\n".join(
        [
            i["name"] if i["alive"] else f"<s>{i['name']}</s>"
            for i in list(players.values())
        ]
    )
    await message.answer(pretty_players)


@router.message(Command("choice"))
async def choice(message: Message):
    players = [{'name': 'first_name', 'id':'12345'}, {'name': 'dimon', 'id':'76345'}]
    await message.answer('Вот тебе инлайн клавиатура со ссылками!', reply_markup=players_kb(players))


    
@router.callback_query(PlayerCallback.filter(F.name))
async def my_callback_foo(query: CallbackQuery, callback_data: PlayerCallback):
    await query.message.answer(f"{callback_data}")
    await query.answer(f"{callback_data}")


