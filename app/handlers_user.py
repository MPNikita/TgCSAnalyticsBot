from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery

from app.texts import START, HELP
import app.keyboards as kb
from database.data import data_tournament


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


@router_user.message(F.text.in_({'Katowice 2024', 'Moscow 2024', 'London 2024'})) #NEED CHANGING
async def first_predict(message: Message):
    for tr in data_tournament:
        if tr['name'] == message.text:
          tournament_id = tr['id']
          break

    await message.answer('Choose winner of the match', reply_markup =await kb.predict_first_match(tournament_id))


@router_user.callback_query(F.data.contains('predict'))
async def predict_macth(callbackquery: CallbackQuery):
    _, match_id, result = callbackquery.data.split('_')
    #todo: save predict
    await callbackquery.answer('Predict Saved')
    await callbackquery.message.answer('Choose winner of the match', reply_markup =await kb.predict_match(int(match_id)))


@router_user.message((F.text == 'Back to menu') | (F.data == 'Menu'))
async def back_to_menu(message: Message):
    await message.answer("Menu", reply_markup = kb.main)