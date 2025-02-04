from random import choice, sample
from typing import Any, ClassVar, List, Optional

from beanie import Document
from config import ROUNDS_DATA


class Game(Document):
    rounds_count: int
    rounds_keys: list[str] = []
    players_ids: List[str] = []
    glitch: Optional[str] = None

    MAX_ROUNDS_COUNT: ClassVar[int] = len(ROUNDS_DATA)

    class Settings:
        name = "games"

    def model_post_init(self, _: Any) -> None:
        self.rounds_keys = sample(list(ROUNDS_DATA), self.rounds_count)

    async def start(self) -> None:
        self.glitch = choice(self.players_ids)
        ...

    async def next_round(self) -> str:
        try:
            message = choice(ROUNDS_DATA[next(self.round_keys)])
        except StopIteration:
            await self.stop()
        ...
        return message

    async def stop(self) -> None: ...
