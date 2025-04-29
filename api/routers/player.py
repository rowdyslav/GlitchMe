from fastapi import APIRouter

from ..schemas import (
    PathPlayerTgId,
    Player,
    QueryPlayerTgId,
    player_not_found,
    player_votes_himself,
)

router = APIRouter(prefix="/player", tags=["Игрок"])


@router.post("/vote/{player_tg_id}", response_model=Player)
async def vote(player_tg_id: PathPlayerTgId, voted_tg_id: QueryPlayerTgId) -> Player:
    if player_tg_id == voted_tg_id:
        raise player_votes_himself

    voted = await Player.find_one(Player.tg_id == voted_tg_id)
    if voted is None:
        raise player_not_found

    voted.votes += 1
    await voted.save()

    return voted


"""
1) Player.votes: int
2) 

"""
