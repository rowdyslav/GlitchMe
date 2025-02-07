from config import MAX_ROUNDS_COUNT, MIN_PLAYERS_COUNT
from fastapi import APIRouter, HTTPException, status
from schemas import Game, GameIdPath, PlayerIdQuery, RoundsCountQuery

router = APIRouter(prefix="/game", tags=["Игра"])
game_not_found = HTTPException(404, "Игра не найдена")


@router.get(
    "/max_rounds_count/",
    summary="Получение максимального возможного количества раундов",
    response_description="Число - максимальное количество раундов",
)
async def max_rounds_count() -> int:
    """Возвращает максимально возможное количество раундов"""

    return MAX_ROUNDS_COUNT


@router.post(
    "/create",
    response_model=Game,
    status_code=status.HTTP_201_CREATED,
    summary="Создание игрового лобби",
    response_description="Созданная запись игры в бд",
)
async def create(rounds_count: RoundsCountQuery) -> Game:
    """Создает объект модели Game, записывает в бд, возвращает созданную запись"""

    return await Game(rounds_count=rounds_count).insert()


@router.post("/connect/{game_id}", summary="Подключение игрока к игре")
async def connect(game_id: GameIdPath, player_id: PlayerIdQuery) -> None:
    """Добавляет айди игрока в массив игроков объекта Game"""

    game = await Game.get(game_id)
    if not game:
        raise game_not_found
    if player_id in game.players_ids:
        raise HTTPException(409, f"{player_id} уже в игре!")

    game.players_ids.append(player_id)
    await game.save()


@router.post(
    "/start/{game_id}",
    summary="Запустить игру",
    response_description="Запись запущенной игры из бд",
)
async def start(game_id: GameIdPath) -> Game:
    """Начинает игру, устанавливая объекту Game поле glitch_player_id"""

    game = await Game.get(game_id)
    if not game:
        raise game_not_found
    if len(game.players_ids) < MIN_PLAYERS_COUNT:
        raise HTTPException(409, "Недостатчно игроков для старта!")

    await game.start()
    return game
