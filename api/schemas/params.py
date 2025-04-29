from typing import Annotated

from beanie import PydanticObjectId
from fastapi import Path, Query

from config import ROUNDS_MAX_COUNT

QueryRoundsCount = Annotated[
    int,
    Query(
        description="Количество раундов",
        example=1,
        ge=1,
        le=ROUNDS_MAX_COUNT,
    ),
]

PathGameId = Annotated[
    PydanticObjectId,
    Path(
        description="Айди игры в базе данных",
        example="5eb7cf5a86d9755df3a6c593",
    ),
]

PathPlayerTgId = Annotated[
    int,
    Path(
        description="Айди игрока в тг",
        example="23213232142134124",
    ),
]

QueryPlayerTgId = Annotated[
    int,
    Query(
        description="Айди игрока в тг",
        example="23213232142134124",
    ),
]
