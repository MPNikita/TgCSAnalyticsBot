from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from app.config import ADMINS
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext 
import database.requests as rq
import app.keyboards as kb


router_admin = Router()


class TournamentCreation(StatesGroup):
    name = State()


class MatchCreation(StatesGroup):
    team1 = State()
    team2 = State()
    creation = State()


class OpenPredicts(StatesGroup):
    open_ = State()


class ClosePredicts(StatesGroup):
    close_ = State()


async def admin_checker(id):
    if id in ADMINS:
        return True
    return False


@router_admin.message(Command('create_tournament'))
async def create_tournament_1(message: Message, state: FSMContext):
    if not await admin_checker(message.from_user.id):
        await message.answer('No permission')
        return
    
    await state.set_state(TournamentCreation.name)
    await message.answer('Enter name of Tournament. Attention, enter only HLTV name of tournament')


@router_admin.message(TournamentCreation.name)
async def create_tournament_2(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text = await rq.new_tournament(message.text))


@router_admin.message(Command('create_match'))
async def create_match_1(message: Message, state: FSMContext):
    if not await admin_checker(message.from_user.id):
        await message.answer('No permission')
        return
    
    await state.set_state(MatchCreation.team1)
    await message.answer('Enter name of Tournament. Attention, enter only HLTV name of tournament!')


@router_admin.message(MatchCreation.team1)
async def create_match_2(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await state.set_state(MatchCreation.team2)
    await message.answer(text = "Enter name of first team from HLTV")


@router_admin.message(MatchCreation.team2)
async def create_match_2(message: Message, state: FSMContext):
    await state.update_data(team1 = message.text)
    await state.set_state(MatchCreation.creation)
    await message.answer(text = "Enter name of second team from HLTV")


@router_admin.message(MatchCreation.creation)
async def create_match_2(message: Message, state: FSMContext):
    await state.update_data(team2 = message.text)
    data = await state.get_data()
    await state.clear()
    await message.answer(text = await rq.new_match(data['name'], data['team1'],data['team2']))


@router_admin.message(Command('open_predicts'))
async def open_1(message: Message, state: FSMContext):
    if not await admin_checker(message.from_user.id):
        await message.answer('No permission')
        return
    
    await state.set_state(OpenPredicts.open_)
    await message.answer("Which tournament to open?", reply_markup = await kb.open_tournament())


@router_admin.message(OpenPredicts.open_)
async def open_2(message: Message, state: FSMContext):
    await rq.open_tournament(message.text)
    await message.answer(text = "Tournament opened")


@router_admin.message(Command('close_predicts'))
async def close_1(message: Message, state: FSMContext):
    if not await admin_checker(message.from_user.id):
        await message.answer('No permission')
        return
    
    await state.set_state(ClosePredicts.close_)
    await message.answer("Which tournament to close?", reply_markup = await kb.close_tournament())


@router_admin.message(ClosePredicts.close_)
async def close_2(message: Message, state: FSMContext):
    await rq.close_tournament(message.text)
    await message.answer(text = "Tournament closed")