from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class PlayerVoteCallback(CallbackData, prefix="player"):
    player_id: int
    name: str
    alive: bool


def players_vote_kb(players):
    inline_kb_list = [
        [
            InlineKeyboardButton(
                text=f"{player['name']}",
                callback_data=PlayerVoteCallback(
                    player_id=f"{player['id']}",
                    name=player["name"],
                    alive=player["alive"],
                ).pack(),
            )
        ]
        for player in players
    ]

    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
