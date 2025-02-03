from typing import Annotated

from beanie import PydanticObjectId
from config import ROUNDS_DATA
from fastapi import APIRouter, HTTPException, status
from models import Game
from pydantic import Field

router = APIRouter(prefix="/games", tags=["Игра"])
game_not_found = HTTPException(404, "Игра не найдена")


@router.post(
    "/create/",
    status_code=status.HTTP_201_CREATED,
    summary="Создание игрового лобби",
    response_description="Созданная запись игры в базе данных",
    response_model=Game,
)
async def create(
    rounds_count: Annotated[int, Field(ge=1, le=len(ROUNDS_DATA))]
) -> Game:
    """Создает объект модели, записывает в базу данных, возвращает"""

    return await Game(rounds_count=rounds_count).insert()


@router.post("/connect/{game_id}")
async def connect(game_id: PydanticObjectId, player_id: str) -> None:
    game = await Game.get(game_id)
    if not game:
        raise game_not_found
    game.players += player_id
    await game.save()


@router.post("/start/{game_id}")
async def start(game_id: PydanticObjectId) -> None:
    game = await Game.get(game_id)
    if not game:
        raise game_not_found
    if len(game.players) < 5:
        raise HTTPException(409, "Недостатчно игроков для старта!")
    await game.start()
