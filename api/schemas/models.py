from random import choice, sample
from typing import Annotated, Any, Generator, Iterable, Iterator, Optional

from beanie import Document, Indexed, PydanticObjectId
from config import ROUNDS_QUESTIONS
from pydantic import BeforeValidator, ConfigDict
from pydantic.main import TupleGenerator


class Player(Document):
    """Модель игрока"""

    name: str
    tg_id: Annotated[int, Indexed(unique=True)]

    class Settings:
        name = "players"


class Game(Document):
    rounds_count: int
    players_ids: list[PydanticObjectId] = []
    glitch_player_id: Optional[PydanticObjectId] = None
    rounds_keys: tuple[str, ...] = ()

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    class Settings:
        name = "games"

    def model_post_init(self, __context: Any) -> None:
        # При СОЗДАНИИ (if чтобы определять) генерируем последовательность ключей в виде итератора
        if not self.rounds_keys:
            self.rounds_keys = tuple(sample(list(ROUNDS_QUESTIONS), self.rounds_count))
        return super().model_post_init(__context)

    async def start(self) -> None:
        # Пример: выбор случайного игрока для glitch
        self.glitch_player_id = choice(self.players_ids)

    async def next_round(self) -> str:
        try:
            message = choice(ROUNDS_QUESTIONS[next(iter(self.rounds_keys))])
        except StopIteration:
            await self.stop()
            message = "Игра окончена."
        return message

    async def stop(self) -> None:
        # Логика завершения игры (например, удаление документа)
        await self.delete()
