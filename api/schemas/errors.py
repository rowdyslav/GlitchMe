from collections import defaultdict
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel

game_not_found = HTTPException(404, "Игра не найдена!")

player_already_connected = HTTPException(409, "Игрок уже подключен к игре!")
not_enough_players = HTTPException(409, "Недостатчно игроков для старта!")


class HTTPError(BaseModel):
    detail: str


class RequestDataError(HTTPError):
    related_errors: dict[str, list[str]]


class ErrorResponsesDict(defaultdict):
    def __init__(
        self,
        *,
        not_found: bool = False,
        conflict: Optional[str] = None,
        unprocessable_entity: bool = False,
        service_unavailable: bool = False,
    ) -> None:
        """not_found 404
        conflict 409
        unprocessable_entity 422
        service_unavailable 503"""

        super().__init__(
            lambda: {"model": HTTPError, "content": {"application/json": {}}}
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
