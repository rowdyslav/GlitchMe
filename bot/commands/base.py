from aiogram import F, Router
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram.utils.deep_linking import decode_payload

from env import APP_URL

from ..misc import (
    PlayerVoteCallback,
    get_game_players,
    player_vote_ikm,
    post_game_connect,
    post_player_vote,
)

router = Router()

players_games_ids: dict[int, str] = {}


@router.message(CommandStart(deep_link=True, magic=F.args))
async def start_link(message: Message, command: CommandObject):
    assert (user := message.from_user) is not None

    args = command.args
    assert args is not None

    uid = user.id
    player_name = user.username or f"{user.first_name}ⁿⁿ"

    game_id = decode_payload(args)
    await post_game_connect(game_id, uid, player_name)
    players_games_ids[uid] = game_id

    await message.answer(f"{player_name}, вы успешно подключились к игре {game_id}!")


@router.message(CommandStart())
async def start(message: Message):
    assert (user := message.from_user) is not None
    player_name = user.username or f"{user.first_name}ⁿⁿ"
    await message.answer(f"Привет, {player_name}!\n/help - помощь")


@router.message(Command(commands=["help", "h", "description"]))
async def help_command(message: Message):
    await message.answer(
        f"""Бот создан для настольной игры GlichMe!
Для запуска необходимо перейти на <a href="{APP_URL}">сайт</a>, создать лобби и перейти по QR-коду.
"""
    )


@router.message(Command("players"))
async def players(message: Message):
    assert (user := message.from_user) is not None
    uid = user.id
    if uid not in players_games_ids:
        await message.answer("Вы не в игре!")
        return
    players = await get_game_players(players_games_ids[uid])
    # id : [name: str, alive: bool]
    pretty_players = "\n".join(
        [i["name"] if i["alive"] else f"<s>{i['name']}</s>" for i in players]
    )
    await message.answer(pretty_players)


@router.message(Command("vote"))
async def vote(message: Message):
    assert (user := message.from_user) is not None
    uid = user.id
    if uid not in players_games_ids:
        await message.answer("Вы не в игре!")
        return
    players = await get_game_players(players_games_ids[uid])
    for player in players:
        if player["tg_id"] == uid:
            player_alive = player["alive"]
            player_voted = player["voted_for_id"] is not None
            if player_voted:
                await message.answer("Вы уже проголосовали в этом раунде!")
                return
            if not player_alive:
                await message.answer("Вас исключили! Вы не можете голосовать(")
                return
    await message.answer("Выбирайте с умом", reply_markup=player_vote_ikm(players))


@router.callback_query(PlayerVoteCallback.filter(F.name))
async def vote_callback(query: CallbackQuery, callback_data: PlayerVoteCallback):
    assert (user := query.from_user) is not None
    uid = user.id

    name = callback_data.name
    voted_id = callback_data.tg_id
    alive = callback_data.alive

    if alive:
        await post_player_vote(uid, voted_id)
        await query.answer(f"Ваш голос был отдан за игрока {name}")
    else:
        await query.answer(f"Выбывшие игроки не могут голосовать")
