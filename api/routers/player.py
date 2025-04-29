from fastapi import APIRouter

from ..schemas import (
    Game,
    PathPlayerTgId,
    Player,
    QueryPlayerTgId,
    player_not_found,
    player_not_in_game,
    player_votes_himself,
)

router = APIRouter(prefix="/player", tags=["Игрок"])


@router.post("/vote/{player_tg_id}", response_model=Player)
async def vote(
    player_tg_id: PathPlayerTgId, voted_tg_id: QueryPlayerTgId
) -> Player: ...
