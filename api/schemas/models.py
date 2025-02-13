from random import choice, sample
from typing import Annotated, Any, Optional

from beanie import Document, Indexed, PydanticObjectId
from config import ROUNDS_QUESTIONS


class Player(Document):
    """Модель игрока"""

    name: str
    tg_id: Annotated[int, Indexed(unique=True)]

    class Settings:
        name = "players"


class Game(Document):
    """Ключевая модель, представляющая игру/лобби на различных стадиях"""

    rounds_count: int
    rounds_keys: tuple[str, ...] = ()
    players_ids: list[PydanticObjectId] = []
    glitch_player_id: Optional[PydanticObjectId] = None

    def model_post_init(self, __context: Any) -> None:
        self.rounds_keys = tuple(sample(list(ROUNDS_QUESTIONS), self.rounds_count))
        return super().model_post_init(__context)

    class Settings:
        name = "games"

    async def start(self) -> None:
        self.glitch_player_id = choice(self.players_ids)
        ...

    async def next_round(self) -> str:
        try:
            message = choice(ROUNDS_QUESTIONS[next(self.round_keys)])
        except StopIteration:
            await self.stop()
        ...
        return message

    async def stop(self) -> None:
        ...
        await self.delete()
