from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from app.texts import WELCOME
import app.keyboards as kb


router_user = Router()


@router_user.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(WELCOME, reply_markup = kb.main)



@router_user.message(Command('help'))
async def cmd_start(message: Message):
    await message.answer("Noone can help us!")
