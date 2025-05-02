from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from ..misc import BASE as _

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(_["welcome"])


@router.message(Command(commands=["h", "help", "description"]))
async def h(message: Message):
    await message.answer(_["help"])
