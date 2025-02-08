from collections import defaultdict
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel


class HTTPError(BaseModel):
    detail: str


class ErrorResponses(defaultdict):
    def __init__(
        self: dict[int, dict[str, type[HTTPError] | str]],
        not_found: bool = False,
        conflict: Optional[str] = None,
        unprocessable_entity: bool = False,
    ) -> None:
        self = defaultdict(lambda: {"model": HTTPError})
        if not_found:
            self[404]["description"] = "Не найдено - игра не существует"
        if conflict is not None:
            self[409]["description"] = f"Конфликт - {conflict}"
        if unprocessable_entity:
            self[422]["description"] = "Неверные данные запроса"
        self = dict(self)


game_not_found = HTTPException(404, "Игра не найдена!")

player_already_connected = HTTPException(409, "Игрок уже подключен к игре!")
not_enough_players = HTTPException(409, "Недостатчно игроков для старта!")
