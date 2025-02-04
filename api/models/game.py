from random import choice, sample
from typing import List, Optional

from beanie import Document
from config import ROUNDS_DATA
from pydantic import computed_field


class Game(Document):
    class Settings:
        name = "games"

    rounds_count: int
    players: List[str] = []
    glitch: Optional[str] = None

    @computed_field
    @property
    def rounds_keys(self) -> List[str]:
        return sample(tuple(ROUNDS_DATA.keys()), self.rounds_count)

    async def start(self) -> None:
        self.glitch = choice(self.players)
        ...

    async def next_round(self) -> str:
        try:
            message = choice(ROUNDS_DATA[next(self.round_keys)])
        except StopIteration:
            await self.stop()
        ...
        return message

    async def stop(self) -> None: ...
