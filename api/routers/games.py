from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException
from models import Game

router = APIRouter(prefix="/games", tags=["Игра"])
game_not_found = HTTPException(404, "Игра не найдена")


@router.post("/create/", response_model=Game)
async def create(rounds_count: int):
    return await Game(rounds_count=rounds_count).insert()


@router.post("/connect/{code}")
async def connect(code: PydanticObjectId, player_id: str):
    game = await Game.get(code)
    if not game:
        raise game_not_found
    game.players += player_id


@router.post("/start/{code}")
async def start(code: PydanticObjectId):
    game = await Game.get(code)
    if not game:
        raise game_not_found
    if len(game.players) < 5:
        raise HTTPException(409, "Недостатчно игроков для старта!")
    await game.start()
