from aiogram import Router
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram.utils.deep_linking import decode_payload

from ..misc import ADVANCED as _
from ..misc import (
    PlayerVoteCallback,
    get_game_players,
    patch_game_connect,
    patch_player_vote,
    player_vote_ikm,
    vote_rkm,
)

router = Router()
users_games: dict[int, str] = {}


async def in_game(message: Message) -> bool:
    """Проверка находится ли юзер в игре"""
    if (u := message.from_user) is None:
        return False
    if u.id not in users_games:
        await message.answer(_["not_in_game"])
        return False
    return True


async def get_player_data(message: Message | CallbackQuery) -> tuple[int, str] | None:
    """Возвращает tg_id и name игрока"""
    if (u := message.from_user) is None:
        return None
    return u.id, u.username or f"{u.first_name}ⁿⁿ"


@router.message(CommandStart(deep_link=True))
async def start_deeplink(message: Message, command: CommandObject):
    if (user_data := await get_player_data(message)) is None or (
        payload := command.args
    ) is None:
        return

    user_id, player_name = user_data
    game_id = decode_payload(payload)

    await patch_game_connect(game_id, user_id, player_name)
    users_games[user_id] = game_id
    await message.answer(
        _["connected"].format(name=player_name, game_id=game_id), reply_markup=vote_rkm
    )


@router.message(Command("players"))
async def players(message: Message):
    if (user_data := await get_player_data(message)) is None:
        return

    if not await in_game(message):
        return

    players = await get_game_players(users_games[user_data[0]])
    await message.answer(
        "\n".join(
            player["name"] if player["alive"] else f"<s>{player['name']}</s>"
            for player in players
        )
    )


@router.message(Command("vote"))
async def vote(message: Message):
    if (user_data := await get_player_data(message)) is None:
        return

    if not await in_game(message):
        return

    user_id = user_data[0]
    game_players = await get_game_players(users_games[user_id])
    current_player = next((p for p in game_players if p["tg_id"] == user_id), None)

    if not current_player:
        await message.answer(_["not_in_game"])
        return

    if current_player["voted_for_id"] is not None:
        await message.answer(_["already_voted"])
        return

    if not current_player["alive"]:
        await message.answer(_["dead_cant_vote"])
        return

    other_players = [p for p in game_players if p["tg_id"] != user_id]
    await message.answer(
        _["vote_instruction"],
        reply_markup=player_vote_ikm(other_players),
    )


@router.callback_query(PlayerVoteCallback.filter())
async def vote_callback(query: CallbackQuery, callback_data: PlayerVoteCallback):
    if (data := await get_player_data(query)) is None:
        return

    if not callback_data.alive:
        await query.answer(_["dead_vote_attempt"])
        return
    from icecream import ic

    ic(data)
    response_status = await patch_player_vote(data[0], callback_data.tg_id)
    if response_status == 200:
        await query.answer(_["vote_accepted"].format(name=callback_data.name))
        if type(message := query.message) is Message:
            await message.answer(_["vote_accepted"].format(name=callback_data.name))
            await message.delete()

    elif response_status == 409:
        await query.answer(str(response_status))
