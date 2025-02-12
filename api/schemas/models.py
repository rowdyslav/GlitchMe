from random import choice, sample
from typing import Optional

from beanie import Document, Link
from config import ROUNDS_QUESTIONS
from pydantic import PrivateAttr


class Player(Document):
    """Модель игрока"""

    name: str
    tg_id: int

    class Settings:
        name = "players"


class Game(Document):
    """Ключевая модель, представляющая игру/лобби на различных стадиях"""

    players: list[Link[Player]] = []
    rounds_keys: tuple[str, ...] = ()
    glitch_player: Optional[Link[Player]] = None

    def __init__(self, rounds_count: int, *args, **kwargs):
        """Инит объекта игры, единственный аргумент - количество раундов"""

        super().__init__(*args, **kwargs)
        self.rounds_keys = tuple(sample(list(ROUNDS_QUESTIONS), rounds_count))

    class Settings:
        name = "games"

    async def start(self) -> None:
        self.glitch_player = choice(self.players)
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
