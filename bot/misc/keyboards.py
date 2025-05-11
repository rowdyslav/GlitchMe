from aiogram.filters.callback_data import CallbackData
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


class PlayerVoteCallback(CallbackData, prefix="player"):
    name: str
    tg_id: int
    alive: int


def player_vote_ikm(players: list[dict]):
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=f"{player['name']}",
                callback_data=PlayerVoteCallback(
                    name=player["name"], tg_id=player["tg_id"], alive=player["alive"]
                ).pack(),
            )
        ]
        for player in players
    ]

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
