from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from app.texts import START, HELP
import app.keyboards as kb


router_user = Router()


@router_user.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(START, reply_markup = kb.main)



@router_user.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(HELP, reply_markup = kb.main)


@router_user.message(F.text == 'Make Prediction')
async def show_tournaments(message: Message):
    await message.answer('Choose tournaments', reply_markup =await kb.choose_tournament())


@router_user.message(F.text == "Back to menu")
async def back_to_menu(message: Message):
    await message.answer("Menu", reply_markup = kb.main)