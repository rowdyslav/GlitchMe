from random import choice, choices
from typing import List

from beanie import Document
from pydantic import computed_field

# from ..config import ROUNDS
ROUNDS = []


class Game(Document):
    rounds_count: int
    players: List[str] = []

    @computed_field
    @property
    def glitch(self) -> str:
        return choice(self.players)

    @computed_field
    @property
    def rounds(self) -> List[str]:
        return choices(ROUNDS, k=self.rounds_count)

    async def start(self):
        pass
