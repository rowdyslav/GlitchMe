from random import choice, sample
from typing import Annotated, Any, Optional, Self

from beanie import Document, Indexed, PydanticObjectId, UpdateResponse
from pydantic import ConfigDict

from config import ROUNDS_QUESTIONS

from ..misc import post_send_messages


class Player(Document):
    """Модель игрока"""

    name: str
    tg_id: Annotated[int, Indexed(unique=True)]
    alive: Optional[bool] = None
    votes: int = -1

    class Settings:
        name = "players"

    @classmethod
    async def get_or_create(cls, data: Self) -> Self:
        return await cls.find_one(Player.tg_id == player_data.tg_id).upsert(  # type: ignore
            {"$set": data.model_dump(exclude={"id"})},
            on_insert=data,
            response_type=UpdateResponse.NEW_DOCUMENT,
        )


class Game(Document):
    rounds_count: int
    players_ids: list[PydanticObjectId] = []
    glitch_player_id: Optional[PydanticObjectId] = None
    rounds_keys: list[str] = []

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    class Settings:
        name = "games"

    def model_post_init(self, __context: Any) -> None:
        self.rounds_keys = sample(list(ROUNDS_QUESTIONS), self.rounds_count)
        return super().model_post_init(__context)

    async def start(self) -> None:
        self.glitch_player_id = choice(self.players_ids)
        await self.next_round()

    async def connect(self, player_id: PydanticObjectId):
        self.players_ids.append(player_id)
        await self.save()

    async def start_voting(self) -> None:
        players = [
            player
            for player_id in self.players_ids
            if (player := await Player.get(player_id)) is not None
        ]
        for player in players:
            player.votes = 0
            await player.save()

    async def stop_voting(self) -> None:
        players = [
            player
            for player_id in self.players_ids
            if (player := await Player.get(player_id)) is not None
        ]
        max(players, key=lambda p: p.votes).alive = False
        for player in players:
            player.votes = -1
            await player.save()
        await self.next_round()

    async def next_round(self) -> None:
        if self.rounds_count == 0:
            await self.stop()
            return

        self.rounds_count -= 1
        round_key = self.rounds_keys.pop(0)
        await self.save()

        question = choice(ROUNDS_QUESTIONS[round_key])
        glitch_question = choice(ROUNDS_QUESTIONS[round_key])
        while question == glitch_question:
            glitch_question = choice(ROUNDS_QUESTIONS[round_key])

        messages = {player_id: question for player_id in self.players_ids}
        assert (gpid := self.glitch_player_id) is not None
        messages[gpid] = glitch_question

        await post_send_messages(messages)

    async def stop(self) -> None:
        # Логика завершения игры
        await self.delete()
