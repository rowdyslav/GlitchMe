from asyncio import create_task, sleep
from random import choice, sample
from typing import Annotated, Any, Optional, Self

from beanie import Document, Indexed, PydanticObjectId, UpdateResponse
from beanie.operators import In, Set

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
        return await cls.find_one(cls.tg_id == data.tg_id).upsert(  # type: ignore
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

    class Settings:
        name = "games"

    def model_post_init(self, __context: Any) -> None:
        if len(self.rounds_keys) != self.rounds_count:
            self.rounds_keys = sample(list(ROUNDS_QUESTIONS), self.rounds_count)
        super().model_post_init(__context)

    async def start(self) -> None:
        await Player.find(In(Player.id, self.players_ids)).update_many(
            Set({Player.alive: True})
        )
        await self.set({Game.glitch_player_id: choice(self.players_ids)})
        await self.set({Game.in_voting: False})
        await self.next_round()

    async def connect(self, player_id: PydanticObjectId):
        if player_id not in self.players_ids:
            self.players_ids.append(player_id)
            await self.save()

    async def players(self) -> list[Player]:
        return await Player.find(In(Player.id, self.players_ids)).to_list()

    async def start_voting(self) -> None:
        await self.set({Game.in_voting: True})
        await post_send_messages(
            [
                (player.name, player.tg_id, player.alive)
                for player in await self.players()
                if player.alive
            ]
        )

    async def stop_voting(self) -> None:
        players = await self.players()

        votes: dict[PydanticObjectId, int] = {}
        for p in players:
            assert (voted_id := p.voted_for_id) is not None
            votes[voted_id] = votes.get(voted_id, 0) + 1

        assert (kicked_player := await Player.get(max(votes.keys()))) is not None
        await kicked_player.set({Player.alive: False})
        await Player.find(In(Player.id, self.players_ids)).update_many(
            Set({Player.voted_for_id: None})
        )
        await self.set({Game.in_voting: False})
        if kicked_player.id == self.glitch_player_id:
            await self.stop()
            return
        await self.next_round()

    async def next_round(self) -> None:
        if self.rounds_count == 0:
            await self.stop()
            return

        self.rounds_count -= 1
        round_key = self.rounds_keys.pop(0)
        await self.save()

        questions = ROUNDS_QUESTIONS[round_key]
        question, glitch_question = sample(questions, 2)

        players = await self.players()
        messages = [
            (
                p.tg_id,
                question if p.id != self.glitch_player_id else glitch_question,
                None,
            )
            for p in players
        ]

        await post_send_messages(messages)

    async def stop(self) -> None:
        async def _():
            await sleep(60)
            await Player.find(In(Player.id, self.players_ids)).update_many(
                Set({Player.alive: None})
            )
            await self.delete()

        create_task(_())
        return
