from typing import Annotated

from beanie import PydanticObjectId
from config import MAX_ROUNDS_COUNT
from fastapi import Path, Query

RoundsCountQuery = Annotated[
    int,
    Query(
        description="Количество раундов",
        example=1,
        ge=1,
        le=MAX_ROUNDS_COUNT,
    ),
]

GameIdPath = Annotated[
    PydanticObjectId,
    Path(
        description="Айди игры в базе данных",
        example="5eb7cf5a86d9755df3a6c593",
    ),
]
