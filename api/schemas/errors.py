from fastapi import HTTPException

game_not_found = HTTPException(404, "Игра не найдена!")

player_already_connected = HTTPException(409, "Игрок уже подключен к игре!")
not_enough_players = HTTPException(409, "Недостатчно игроков для старта!")
