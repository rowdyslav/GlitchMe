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
    voted_for_id: Optional[PydanticObjectId] = None

    class Settings:
        name = "players"

    @classmethod
    async def get_or_create(cls, data: Self) -> Self:
        return await cls.find_one(Player.tg_id == data.tg_id).upsert(  # type: ignore
            {"$set": data.model_dump(exclude={"id"})},
            on_insert=data,
            response_type=UpdateResponse.NEW_DOCUMENT,
        )


class Game(Document):
    rounds_count: int
    players_ids: list[PydanticObjectId] = []
    glitch_player_id: Optional[PydanticObjectId] = None
    in_voting: Optional[bool] = None
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
        for player in await self.players():
            player.alive = True
            await player.save()
        self.glitch_player_id = choice(self.players_ids)
        await self.next_round()

    async def connect(self, player_id: PydanticObjectId):
        self.players_ids.append(player_id)
        await self.save()

    async def players(self) -> list[Player]:
        return [
            player
            for player_id in self.players_ids
            if (player := await Player.get(player_id)) is not None
        ]

    async def start_voting(self) -> None:
        self.in_voting = True
        await self.save()

    async def stop_voting(self) -> None:
        players = await self.players()
        players_votes = (
            (voted, len([... for player in players if player.voted_for_id == voted.id]))
            for voted in players
        )
        max(players_votes, key=lambda v: v[1])[0].alive = False
        for player in players:
            player.voted_for_id = None
            await player.save()
        self.in_voting = False
        await self.next_round()

    async def next_round(self) -> None:
        if self.rounds_count == 0:
            await self.stop()
            return

        self.rounds_count -= 1
        round_key = self.rounds_keys.pop(0)
        await self.save()

        q = lambda: choice(ROUNDS_QUESTIONS[round_key])
        question = q()
        glitch_question = q()
        while question == glitch_question:
            glitch_question = q()

        messages = {
            player_tg_id: question
            for player_tg_id in [player.tg_id for player in await self.players()]
        }
        assert (glitch := await Player.get(self.glitch_player_id)) is not None
        messages[glitch.tg_id] = glitch_question

        await post_send_messages(messages)

    async def stop(self) -> None:
        for player in await self.players():
            player.alive = None
            await player.save()
        await self.delete()
