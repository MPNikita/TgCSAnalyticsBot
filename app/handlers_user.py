from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext 

from app.texts import START, HELP, ABOUT_US
import app.keyboards as kb
import database.requests as rq
import app.states as st


router_user = Router()


@router_user.message(CommandStart())
async def cmd_start(message: Message):
    await rq.new_user(message.from_user.id, message.from_user.username)
    await message.answer(START, reply_markup = kb.main)



@router_user.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(HELP, reply_markup = kb.main)


@router_user.message(F.text == 'Провести мощнейшую аналитику')
async def show_tournaments(message: Message, state: FSMContext):
    tornaments = list(await rq.opened_tournaments())
    if not tornaments:
        await message.answer('Нет турниров для проведения мощнейшей аналитики', reply_markup = kb.main)
    else:
        await state.set_state(st.InitPred.init)
        await message.answer('Выберите турнир', reply_markup =await kb.choose_tournament())


@router_user.message(st.InitPred.init) 
async def choose_tournament(message: Message, state: FSMContext):
    tournament = await rq.find_tournament_by_name(message.text)
    await state.clear()
    if message.text != "Вернуться в меню":
        await message.answer('Кто победит в этом матче?', reply_markup =await kb.predict_match(tournament.id, 0))
    else:
        await message.answer(text = 'Меню', reply_markup = kb.main)


@router_user.callback_query(F.data.contains('predict'))
async def predict_macth(callbackquery: CallbackQuery):
    _, match_id, tournament_id, match_local_id, result, exists_next = callbackquery.data.split('_')
    await rq.new_predict(callbackquery.from_user.id, int(match_id), int(result))
    await callbackquery.answer('Прогноз сохранен')

    if exists_next == 'no':
        await callbackquery.message.answer('Все прогнозы на этот турнир сделаны', reply_markup = kb.main)
        return
    
    match_local_id = int(match_local_id) + 1
    await callbackquery.message.edit_text('Кто победит в этом матче?', reply_markup =await kb.predict_match(int(tournament_id), int(match_local_id)))


@router_user.message(F.text == 'Рейтинг аналитиков')
async def show_leaderboard_1(message: Message, state: FSMContext):
    await state.set_state(st.ShowLeaders.show_lead)
    await message.answer("Выберите нужный топ", reply_markup = await kb.show_leaderboards()) #NEED CHANGING


@router_user.message(st.ShowLeaders.show_lead) 
async def show_leaderboard_2(message: Message, state: FSMContext):
    await state.clear()
    top = await rq.get_leaderboard(message.text)

    if message.text == "Мощнейший всеобщий топ":
        top_text = "Мощнейший всеобщий топ\n"
    else:
        top_text = f"Мощнейший топ {message.text}\n"

    place = 1
    for user_top in top:
        wr = user_top.correct_predictions / user_top.number_of_predictions * 100
        user = await rq.get_user_by_id(user_top.user_id)
        top_str = f'{place}. @{user.username} {user_top.correct_predictions}/{user_top.number_of_predictions} {wr:.2f}%\n'
        top_text += top_str
        place += 1
    
    await message.answer(text = top_text, reply_markup = kb.main)


@router_user.message(F.text == 'О нас')
async def show_about_us(message: Message):
    await message.answer(ABOUT_US)


@router_user.callback_query(F.data == 'Меню')
async def back_to_menu2(callbackquery: CallbackQuery):
    await callbackquery.answer('')
    await callbackquery.message.answer("Меню", reply_markup = kb.main)


@router_user.message(F.text == 'Вернуться в меню')
async def back_to_menu2(message: Message):
    await message.answer("Меню", reply_markup = kb.main)
