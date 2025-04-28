from beanie import UpdateResponse
from fastapi import APIRouter, Response, status

from ..misc import generate_qr, get_game_connect_link, post_send_messages
from ..schemas import (
    ErrorResponsesDict,
    Game,
    GameIdPath,
    Player,
    RoundsCountQuery,
    game_not_found,
    not_enough_players,
    player_already_connected,
)

router = APIRouter(prefix="/game", tags=["Игра"])


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    summary="Создать лобби",
    response_description="QR-код для подключения к игре",
    responses={
        201: {"content": {"image/*": {}}},
        **ErrorResponsesDict(unprocessable_entity=True, service_unavailable=True),
    },
    response_class=Response,
)
async def create(rounds_count: RoundsCountQuery) -> Response:
    """Создает объект модели Game, записывает в бд, возвращает QR-код для подключения к игре"""

    game = await Game(rounds_count=rounds_count).insert()
    assert (game_id := game.id)
    qr_bytes, qr_mime = generate_qr(await get_game_connect_link(game_id))
    return Response(
        qr_bytes,
        status.HTTP_201_CREATED,
        {"game_id": str(game_id), "game_players_min_count": str(game.rounds_count + 2)},
        f"image/{qr_mime}",
    )


@router.post(
    "/connect/{game_id}",
    summary="Подключить игрока",
    response_description="Запись игрока из бд",
    responses=ErrorResponsesDict(
        not_found=True, conflict="игрок уже в игре", unprocessable_entity=True
    ),
)
async def connect(game_id: GameIdPath, player_data: Player) -> Player:
    """Находит или регистрирует игрока, добавляет ссылку на него в массив игроков объекта Game"""

    game = await Game.get(game_id)
    if game is None:
        raise game_not_found

    player = await Player.find_one(Player.tg_id == player_data.tg_id).upsert(  # type: ignore
        {"$set": player_data.model_dump(exclude={"id"})},
        on_insert=player_data,
        response_type=UpdateResponse.NEW_DOCUMENT,
    )
    assert (
        type(player) is Player and (player_id := player.id) is not None
    )  # Приходится из за "type: ignore" выше

    if player_id in game.players_ids:
        raise player_already_connected

    game.players_ids.append(player_id)
    await game.save()
    return player


@router.post(
    "/start/{game_id}",
    response_model=Game,
    summary="Запустить",
    response_description="Обновленная запись из бд",
    responses=ErrorResponsesDict(
        not_found=True,
        conflict="недостатчно игроков для старта",
        unprocessable_entity=True,
    ),
)
async def start(game_id: GameIdPath) -> Game:
    """Начинает игру, устанавливая объекту Game поле glitch_player_id"""

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
    summary="Игроки",
    response_description="Список игроков",
    responses=ErrorResponsesDict(not_found=True),
)
async def players(game_id: GameIdPath) -> list[Player]:
    game = await Game.get(game_id)
    if game is None:
        raise game_not_found
    return [
        player
        for player_id in game.players_ids
        if (player := await Player.get(player_id)) is not None
    ]


@router.post(
    "/next_round/{game_id}",
    response_model=Game,
    summary="Следующий раунд",
    response_description="response_description",
    responses=ErrorResponsesDict(not_found=True, unprocessable_entity=True),
)
async def next_round(game_id: GameIdPath) -> Game:
    """Оперирует следующий раунд игры"""

    game = await Game.get(game_id)
    if game is None:
        raise game_not_found

    await game.next_round()
    return game
