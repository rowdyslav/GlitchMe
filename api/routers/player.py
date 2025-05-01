from fastapi import APIRouter

from ..schemas import (
    Game,
    PathPlayerTgId,
    Player,
    QueryPlayerTgId,
    player_already_voted,
    player_not_alive,
    player_not_found,
    player_not_in_game,
    player_votes_himself,
)

router = APIRouter(prefix="/player", tags=["Игрок"])


@router.post("/vote/{player_tg_id}", response_model=Player)
async def vote(player_tg_id: PathPlayerTgId, voted_tg_id: QueryPlayerTgId) -> Player:
    player = await Player.find_one(Player.tg_id == player_tg_id)
    voted = await Player.find_one(Player.tg_id == voted_tg_id)
    if player is None or voted is None:
        raise player_not_found

    game = next(
        game
        for game in await Game.find().to_list()
        if player.id in game.players_ids and voted.id in game.players_ids
    )

    if player.alive is None or game is None:
        raise player_not_in_game

    if not player.alive:
        raise player_not_alive

    if player.voted_for_id is not None:
        raise player_already_voted

    if player == voted:
        raise player_votes_himself

    player.voted_for_id = voted.id
    await player.save()

    return player
