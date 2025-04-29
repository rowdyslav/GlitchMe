from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder


class PlayerVoteCallback(CallbackData, prefix="player"):
    player_id: int



def player_vote_ikm(players):
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=f"{player['name']}",
                callback_data=PlayerVoteCallback(
                    player_id=player['id'],
                ).pack(),
            )
        ]
        for player in players
    ]

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
