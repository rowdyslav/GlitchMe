from aiogram import Bot
from aiogram.utils.deep_linking import create_start_link
from beanie import PydanticObjectId


async def generate_game_link(bot: Bot, game_id: PydanticObjectId) -> str:
    """Принимает id игры, возвращает ссылку для вступления"""

    return await create_start_link(bot, str(game_id), encode=True)
