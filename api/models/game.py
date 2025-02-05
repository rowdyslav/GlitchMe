from random import choice, sample
from typing import Annotated, Any, ClassVar, Optional

from beanie import Document
from config import ROUNDS_DATA
from pydantic import Field


class Game(Document):
    """Ключевая модель, представляющая игру/лобби на различных стадиях"""

    rounds_count: Annotated[int, Field(frozen=True)]

    players_ids: list[int] = []
    rounds_keys: Annotated[tuple[str, ...], Field(frozen=True)] = ()
    glitch_player_id: Annotated[Optional[int], Field(frozen=True)] = None

    MAX_ROUNDS_COUNT: ClassVar[int] = len(ROUNDS_DATA)

    def model_post_init(self, _: Any):
        object.__setattr__(
            self, "rounds_keys", tuple(sample(list(ROUNDS_DATA), self.rounds_count))
        )

    class Settings:
        name = "games"

    async def start(self) -> None:
        self.glitch_player_id = choice(self.players_ids)
        ...

    async def next_round(self) -> str:
        try:
            message = choice(ROUNDS_DATA[next(self.round_keys)])
        except StopIteration:
            await self.stop()
        ...
        return message

    async def stop(self) -> None: ...
