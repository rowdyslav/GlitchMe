from functools import lru_cache

from config import MAX_ROUNDS_COUNT, MIN_PLAYERS_COUNT
from fastapi import APIRouter, status
from schemas import (
    ErrorResponses,
    Game,
    GameIdPath,
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
    response_model=Game,
    status_code=status.HTTP_201_CREATED,
    summary="Создать лобби",
    response_description="Созданная в бд запись",
    responses=ErrorResponses(unprocessable_entity=True),
)
async def create(rounds_count: RoundsCountQuery) -> Game:
    """Создает объект модели Game, записывает в бд, возвращает созданную запись"""

    await Game(rounds_count=rounds_count).insert()

    return qrcode_image_data


@router.post(
    "/connect/{game_id}",
    response_model=None,
    summary="Подключить игрока",
    responses=ErrorResponses(True, "игрок уже в игре", True),
)
async def connect(game_id: GameIdPath, player: Player) -> None:
    """Добавляет айди игрока в массив игроков объекта Game"""

    game = await Game.get(game_id)
    if not game:
        raise game_not_found

    await player.replace()
    player_link = Player.link_from_id(player.id)
    if player_link in game.players:
        raise player_already_connected

    game.players.append(player_link)
    await game.save()


@router.post(
    "/start/{game_id}",
    response_model=Game,
    summary="Запустить",
    response_description="Обновленная запись из бд",
    responses=ErrorResponses(True, "недостатчно игроков для старта", True),
)
async def start(game_id: GameIdPath) -> Game:
    """Начинает игру, устанавливая объекту Game поле glitch_player_id"""

    game = await Game.get(game_id)
    if not game:
        raise game_not_found
    if len(game.players) < MIN_PLAYERS_COUNT:
        raise not_enough_players

    await game.start()
    return game
