from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class PlayerCallbackFactory(CallbackData, prefix="player"):
    player_id: str
    name: str

def players_kb(players):
    inline_kb_list =[
            [InlineKeyboardButton(text=f"{player['name']}", callback_data=PlayerCallbackFactory( player_id=f"{player['id']}", name=player['name']).pack())]
        for player in players]
    
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)




# dun_w это префикс, его можно ловить и стандартным text_startswith=...
# cd_walk = CallbackData("dun_w", "action", "floor")


# @dp.message_handler(commands=['start'])
# async def start(message: types.Message):
#     markup = InlineKeyboardMarkup(row_width=2).add(
#         InlineKeyboardButton(f"Налево",
#                              callback_data=cd_walk.new(
#                                  action='1',
#                                  floor=2
#                              )),
#         InlineKeyboardButton(f"Направо",
#                              callback_data=cd_walk.new(
#                                  action='2',
#                                  floor=2
#                              ))
#     )
#     await message.answer("text", reply_markup=markup)



