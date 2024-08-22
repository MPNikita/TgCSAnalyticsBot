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
        await state.set_state(st.Predict.show_tornament)
        await message.answer('Выберите турнир', reply_markup =await kb.choose_tournament())


@router_user.message(st.Predict.show_tornament) 
async def choose_tournament(message: Message, state: FSMContext):
    tournament = await rq.find_tournament_by_name(message.text)
    
    if message.text != "Вернуться в меню":
        await state.set_state(st.Predict.make_predict)
        await message.answer('Кто победит в этом матче?', reply_markup =await kb.predict_match(tournament.id, 0))
    else:
        await state.clear()
        await message.answer(text = 'Меню', reply_markup = kb.main)


@router_user.callback_query(st.Predict.make_predict)
async def predict_macth(callbackquery: CallbackQuery, state: FSMContext):
    _, match_id, tournament_id, match_local_id, result, exists_next = callbackquery.data.split('_')
    if not await rq.open_check(int(tournament_id)):
        await state.clear()
        await callbackquery.answer('Что-то пошло не так')
        await callbackquery.message.answer('Прогнозы на матчи этого турнира закрыты')
        return

    await rq.new_predict(callbackquery.from_user.id, int(match_id), int(result))
    await callbackquery.answer('Прогноз сохранен')

    if exists_next == 'no':
        await state.clear()
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

    place = 0
    coun = 0
    prev_num = 0
    prev_corr = 0
    flag = False
    for user_top in top:
        wr = user_top.correct_predictions / user_top.number_of_predictions * 100
        user = await rq.get_user_by_id(user_top.user_id)
        if not flag:
            prev_num = user_top.number_of_predictions
            prev_corr = user_top.correct_predictions
            flag = True
            place += 1
        place += 1
        coun += 1
        if prev_num == user_top.number_of_predictions and prev_corr == user_top.correct_predictions:
            place -= 1
        elif place != coun:
            place = coun
        top_str = f'{place}. @{user.username} {user_top.correct_predictions}/{user_top.number_of_predictions} {wr:.2f}%\n'
        top_text += top_str
        prev_num = user_top.number_of_predictions
        prev_corr = user_top.correct_predictions

    
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
