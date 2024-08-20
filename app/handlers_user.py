from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext 

from app.texts import START, HELP
import app.keyboards as kb
import database.requests as rq


router_user = Router()


class InitPred(StatesGroup):
    init = State()


@router_user.message(CommandStart())
async def cmd_start(message: Message):
    await rq.new_user(message.from_user.id, message.from_user.username)
    await message.answer(START, reply_markup = kb.main)



@router_user.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(HELP, reply_markup = kb.main)


@router_user.message(F.text == 'Make Prediction')
async def show_tournaments(message: Message, state: FSMContext):
    await state.set_state(InitPred.init)
    await message.answer('Choose tournaments', reply_markup =await kb.choose_tournament())


@router_user.message(InitPred.init) 
async def first_predict(message: Message, state: FSMContext):
    tournament = await rq.find_tournament_by_name(message.text)
    await state.clear()
    await message.answer('Choose winner of the match', reply_markup =await kb.predict_match(tournament.id, 0))


@router_user.callback_query(F.data.contains('predict'))
async def predict_macth(callbackquery: CallbackQuery):
    _, match_id, tournament_id, match_local_id, result, exists_next = callbackquery.data.split('_')
    await rq.new_predict(callbackquery.from_user.id, int(match_id), int(result))
    await callbackquery.answer('Predict Saved')

    if exists_next == 'no':
        await callbackquery.message.answer('All predicts on this tournament are made', reply_markup = kb.main)
        return
    
    match_local_id = int(match_local_id) + 1
    await callbackquery.message.edit_text('Choose winner of the match', reply_markup =await kb.predict_match(int(tournament_id), int(match_local_id)))


@router_user.message(F.text == 'Back to menu')
async def back_to_menu1(message: Message):
    await message.answer("Menu", reply_markup = kb.main)


@router_user.message(F.text == 'Leaderboard')
async def show_leaderboard(message: Message):
    await message.answer("Sorry, function is underconstraction")


@router_user.message(F.text == 'About Us')
async def show_about_us(message: Message):
    await message.answer("Sorry, function is underconstraction")


@router_user.callback_query(F.data == 'Menu')
async def back_to_menu2(callbackquery: CallbackQuery):
    await callbackquery.answer('')
    await callbackquery.message.answer("Menu", reply_markup = kb.main)
