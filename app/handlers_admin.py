from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from app.config import ADMINS


router_admin = Router()


async def admin_checker(id):
    if id in ADMINS:
        return True
    return False


@router_admin.message(Command('create_tournament'))
async def cmd_help(message: Message):
    if not await admin_checker(message.from_user.id):
        await message.answer('No permission')
        return
    
    await message.answer('Enter name of Tournament. Attention, enter only HLTV name of tournament')


