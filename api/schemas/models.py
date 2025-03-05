from random import choice, sample
from typing import Annotated, Any, Optional

from beanie import Document, Indexed, PydanticObjectId
from pydantic import ConfigDict

from config import ROUNDS_QUESTIONS


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
        self.rounds_keys = tuple(sample(list(ROUNDS_QUESTIONS), self.rounds_count))
        self._rounds = iter(self.rounds_keys)
        return super().model_post_init(__context)

    async def start(self) -> None:
        self.glitch_player_id = choice(self.players_ids)

    async def next_round(self) -> str:
        try:
            message = choice(ROUNDS_QUESTIONS[next(self._rounds)])
        except StopIteration:
            await self.stop()
            message = "Игра окончена"
        return message

    async def stop(self) -> None:
        # Логика завершения игры
        await self.delete()
