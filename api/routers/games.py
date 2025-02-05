from random import randint
from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Query, status
from models import Game

router = APIRouter(prefix="/games", tags=["Игра"])
game_not_found = HTTPException(404, "Игра не найдена")


@router.get(
    "/max_rounds_count/",
    summary="Получение максимального возможного количества раундов",
    response_description="Число - максимальное количество раундов",
)
async def max_rounds_count() -> int:
    """Возвращает константу модели Game - максимальное количество раундов"""

    return Game.MAX_ROUNDS_COUNT


@router.post(
    "/create",
    response_model=Game,
    status_code=status.HTTP_201_CREATED,
    summary="Создание игрового лобби",
    response_description="Созданная запись игры в базе данных",
)
async def create(
    rounds_count: Annotated[
        int,
        Query(
            description="Количество раундов",
            example=randint(1, Game.MAX_ROUNDS_COUNT),
            ge=1,
            le=Game.MAX_ROUNDS_COUNT,
        ),
    ]
) -> Game:
    """Создает объект модели, записывает в базу данных, возвращает"""

    return await Game(rounds_count=rounds_count).insert()


@router.post(
    "/connect/{game_id}",
    summary="Подключение игрока к игре",
)
async def connect(game_id: PydanticObjectId, player_id: int) -> None:
    """Добавляет айди игрока, в массив игроков объекта Game"""

    game = await Game.get(game_id)
    if not game:
        raise game_not_found
    if player_id in game.players_ids:
        raise HTTPException(409, f"{player_id} уже в игре!")

    game.players_ids.append(player_id)
    await game.save()


@router.post("/start/{game_id}")
async def start(game_id: PydanticObjectId) -> None:
    game = await Game.get(game_id)
    if not game:
        raise game_not_found
    if len(game.players_ids) < 5:
        raise HTTPException(409, "Недостатчно игроков для старта!")

    return await game.start()
