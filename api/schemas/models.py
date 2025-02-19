import random
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

    def __next__(self) -> str:
        return next(iter(self.rounds_keys))

    class Settings:
        name = "games"

    def model_post_init(self, __context: Any) -> None:
        # При инициализации генерируем последовательность ключей в виде итератора
        self.rounds_keys = tuple(
            random.sample(list(ROUNDS_QUESTIONS), self.rounds_count)
        )
        from icecream import ic

        ic(list(self.rounds_keys), self.rounds_count)
        return super().model_post_init(__context)

    async def start(self) -> None:
        # Пример: выбор случайного игрока для glitch
        self.glitch_player_id = random.choice(self.players_ids)

    async def next_round(self) -> str:
        try:
            message = random.choice(ROUNDS_QUESTIONS[next(self)])
        except StopIteration:
            await self.stop()
            message = "Игра окончена."
        return message

    async def stop(self) -> None:
        # Логика завершения игры (например, удаление документа)
        await self.delete()
