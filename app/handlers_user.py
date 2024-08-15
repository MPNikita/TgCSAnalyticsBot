from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from app.texts import WELCOME


router_user = Router()


@router_user.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(WELCOME)


@router_user.message(Command('help'))
async def cmd_start(message: Message):
    await message.answer("Noone can help us!")
