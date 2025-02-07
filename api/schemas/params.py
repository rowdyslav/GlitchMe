from random import randint
from typing import Annotated

from beanie import PydanticObjectId
from config import MAX_ROUNDS_COUNT
from fastapi import Path, Query

RoundsCountQuery = Annotated[
    int,
    Query(
        description="Количество раундов",
        example=randint(1, MAX_ROUNDS_COUNT),
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

PlayerIdQuery = Annotated[int, Query(description="Айди игрока в тг", example=123456789)]
