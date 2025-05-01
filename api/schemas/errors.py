from collections import defaultdict
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel

game_not_found = HTTPException(404, "Игра не найдена!")
player_not_found = HTTPException(404, "Игрок не найден!")
player_not_in_game = HTTPException(404, "Игрок не в игре или не существует!")


player_already_connected = HTTPException(409, "Игрок уже подключен к игре!")
not_enough_players = HTTPException(409, "Недостатчно игроков для старта!")
player_not_alive = HTTPException(409, "Игрок исключен!")
player_already_voted = HTTPException(409, "Игрок уже проголосовал!")
player_votes_himself = HTTPException(409, "Игрок голосует за себя!")


class HTTPError(BaseModel):
    detail: str


class RequestDataError(HTTPError):
    related_errors: dict[str, list[str]]


class ErrorResponsesDict(defaultdict):
    """Словарь для поля responses в эндпойнтах FastAPI. Инициализируется с помощью ключевых аргументов, представляющих HTTP ошибки"""

    def __init__(
        self,
        *,
        not_found: bool = False,
        conflict: Optional[str] = None,
        unprocessable_entity: bool = False,
        service_unavailable: bool = False,
    ) -> None:
        """Аргумент: Код ошибки\n
        not_found 404
        conflict 409
        unprocessable_entity 422
        service_unavailable 503"""

        super().__init__(
            lambda: {"content": {"application/json": {}}, "model": HTTPError}
        )
        if not_found:
            self[404]["description"] = "Не найдено - игра не существует"
        if conflict is not None:
            self[409]["description"] = f"Конфликт - {conflict}"
        if unprocessable_entity:
            self[422]["model"] = RequestDataError
            self[422]["description"] = "Error: Validation Error"
        if service_unavailable:
            self[503]["description"] = "Error: Service Unavailable"
