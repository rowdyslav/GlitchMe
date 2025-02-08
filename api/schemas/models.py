from random import choice, sample
from typing import Optional

from beanie import Document
from config import ROUNDS_QUESTIONS


class Game(Document):
    """Ключевая модель, представляющая игру/лобби на различных стадиях"""

    rounds_count: int
    rounds_keys: tuple[str, ...] = ()
    players_ids: list[int] = []
    glitch_player_id: Optional[int] = None

    def model_post_init(self, _) -> None:
        self.rounds_keys = tuple(sample(list(ROUNDS_QUESTIONS), self.rounds_count))

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
