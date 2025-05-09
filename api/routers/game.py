from fastapi import APIRouter, Response, status

from ..misc import generate_qr, get_game_connect_link
from ..schemas import (
    ErrorResponsesDict,
    Game,
    PathGameId,
    Player,
    QueryRoundsCount,
    game_not_found,
    not_enough_players,
    player_already_connected,
)

router = APIRouter(prefix="/game", tags=["Игра"])


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    summary="Создать игру",
    response_description="QR-код для подключения к игре",
    responses={
        201: {"content": {"image/*": {}}},
        **ErrorResponsesDict(unprocessable_entity=True, service_unavailable=True),
    },
    response_class=Response,
)
async def create(rounds_count: QueryRoundsCount) -> Response:
    """Создает игру в бд, возвращает QR-код для подключения"""

    game = await Game(rounds_count=rounds_count).insert()
    assert (game_id := game.id)
    qr_bytes, qr_mime = generate_qr(await get_game_connect_link(game_id))
    return Response(
        qr_bytes,
        status.HTTP_201_CREATED,
        {"game_id": str(game_id), "game_players_min_count": str(game.rounds_count + 2)},
        f"image/{qr_mime}",
    )


@router.patch(
    "/connect/{game_id}",
    summary="Подключить игрока",
    response_description="Обновленная запись игры из бд",
    responses=ErrorResponsesDict(
        not_found="игра", conflict="игрок уже в игре", unprocessable_entity=True
    ),
)
async def connect(game_id: PathGameId, player_data: Player) -> Game:
    """Находит или регистрирует игрока, добавляет его в игру"""

    game = await Game.get(game_id)
    if game is None:
        raise game_not_found

    player = await Player.get_or_create(player_data)
    assert (pid := player.id) is not None

    if pid in game.players_ids:
        raise player_already_connected

    await game.connect(pid)

    return game


@router.post(
    "/start/{game_id}",
    response_model=Game,
    summary="Запустить",
    response_description="Обновленная запись игры из бд",
    responses=ErrorResponsesDict(
        not_found="игра",
        conflict="недостатчно игроков для старта",
        unprocessable_entity=True,
    ),
)
async def start(game_id: PathGameId) -> Game:
    """Начинает игру"""

    game = await Game.get(game_id)
    if game is None:
        raise game_not_found
    if len(game.players_ids) < game.rounds_count + 2:
        raise not_enough_players

    await game.start()

    return game


@router.get(
    "/players/{game_id}",
    response_model=list[Player],
    summary="Список игроков",
    response_description="Список записей игроков из бд",
    responses=ErrorResponsesDict(not_found="игра", unprocessable_entity=True),
)
async def players(game_id: PathGameId, response: Response) -> list[Player]:
    """Получает список игроков или победителей, если игра завершена"""
    game = await Game.get(game_id)
    if game is None:
        raise game_not_found
    players = await game.players()

    if game.in_voting is None:
        return players

    alive_players = [p for p in players if p.alive]
    glitch = next(p for p in players if p.id == game.glitch_player_id)
    ga = glitch.alive

    if ga and len(alive_players) > 2:
        return players

    response.headers["game_ended"] = ""
    return [glitch] if ga else alive_players


@router.post(
    "/start_voting/{game_id}",
    response_model=Game,
    summary="Начать голосование",
    response_description="Обновленная запись игры из бд",
    responses=ErrorResponsesDict(not_found="игра", unprocessable_entity=True),
)
async def start_voting(game_id: PathGameId) -> Game:
    """Начинает голосование"""

    game = await Game.get(game_id)
    if game is None:
        raise game_not_found

    await game.start_voting()
    return game
