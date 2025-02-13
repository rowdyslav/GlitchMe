from functools import lru_cache

from beanie import UpdateResponse
from config import MAX_ROUNDS_COUNT, MIN_PLAYERS_COUNT
from fastapi import APIRouter, Response, status
from misc import from_bot, qr
from schemas import (
    ErrorResponses,
    Game,
    GameIdPath,
    ImageResponse,
    Player,
    RoundsCountQuery,
    game_not_found,
    not_enough_players,
    player_already_connected,
)

router = APIRouter(prefix="/game", tags=["Игра"])


@lru_cache(maxsize=None)
@router.get(
    "/max_rounds_count/",
    response_model=int,
    summary="Получить максимальное возможное количество раундов",
    response_description="Число - максимальное количество раундов",
)
async def max_rounds_count() -> int:
    """Возвращает максимально возможное количество раундов"""

    return MAX_ROUNDS_COUNT


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    summary="Создать лобби",
    response_description="QR код для подключения к игре",
    responses=ErrorResponses(unprocessable_entity=True),
    response_class=ImageResponse,
)
async def create(rounds_count: RoundsCountQuery) -> Response:
    """Создает объект модели Game, записывает в бд, возвращает qr код для подключения к игре"""

    game = await Game(rounds_count=rounds_count).insert()
    assert (game_id := game.id)
    qr_bytes, qr_mime = qr.generate(await from_bot.get_game_link(game_id))
    return Response(
        qr_bytes,
        status.HTTP_201_CREATED,
        media_type=f"image/{qr_mime}",
    )


@router.post(
    "/connect/{game_id}",
    summary="Подключить игрока",
    responses=ErrorResponses(
        not_found=True, conflict="игрок уже в игре", unprocessable_entity=True
    ),
)
async def connect(game_id: GameIdPath, player_data: Player) -> Player:
    """Находит или регистрирует игрока, добавляет ссылку на него в массив игроков объекта Game"""

    game = await Game.get(game_id)
    if not game:
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
    responses=ErrorResponses(
        not_found=True,
        conflict="недостатчно игроков для старта",
        unprocessable_entity=True,
    ),
)
async def start(game_id: GameIdPath) -> Game:
    """Начинает игру, устанавливая объекту Game поле glitch_player_id"""

    game = await Game.get(game_id)
    if not game:
        raise game_not_found
    if len(game.players_ids) < MIN_PLAYERS_COUNT:
        raise not_enough_players

    await game.start()
    return game
