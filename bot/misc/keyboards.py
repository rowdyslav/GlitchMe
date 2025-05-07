from aiogram.filters.callback_data import CallbackData
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from beanie import PydanticObjectId


class PlayerVoteCallback(CallbackData, prefix="player"):
    _id: PydanticObjectId
    tg_id: int
    alive: int
    voted_for_id: PydanticObjectId | None
    name: str


def player_vote_ikm(players: list[dict]):
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=f"{player['name']}",
                callback_data=PlayerVoteCallback(**player).pack(),
            )
        ]
        for player in players
    ]

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


vote_rkm = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="/vote")]], resize_keyboard=True
)
