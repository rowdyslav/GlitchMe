from collections import defaultdict
from typing import Optional

from fastapi import Response
from pydantic import BaseModel


class ImageResponse(Response):
    media_type = "image/*"


class HTTPError(BaseModel):
    detail: str


class ErrorResponses(defaultdict):
    def __init__(
        self,
        *,
        not_found: bool = False,
        conflict: Optional[str] = None,
        unprocessable_entity: bool = False,
    ) -> None:
        """404 not_found
        409 conflict
        422 unprocessable_entity"""

        super().__init__(lambda: {"model": HTTPError})
        if not_found:
            self[404]["description"] = "Не найдено - игра не существует"
        if conflict is not None:
            self[409]["description"] = f"Конфликт - {conflict}"
        if unprocessable_entity:
            self[422]["description"] = "Неверные данные запроса"
