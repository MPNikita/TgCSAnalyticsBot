from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext 

from app.texts import START, HELP, ABOUT_US
import app.keyboards as kb
import database.requests as rq
import app.states as st


router_user = Router()


@router_user.message(CommandStart())
async def cmd_start(message: Message):
    try:
        await rq.new_user(message.from_user.id, message.from_user.username)
        await message.answer(START, reply_markup = kb.main)
    except:
        await message.answer("Что-то пошло не так. Напишите об этом @generalfy")


@router_user.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(HELP, reply_markup = kb.main)


@router_user.message(F.text == 'Провести мощнейшую аналитику')
async def show_tournaments(message: Message, state: FSMContext):
    tornaments = list(await rq.opened_tournaments())
    if not tornaments:
        await message.answer('Нет турниров для проведения мощнейшей аналитики', reply_markup = kb.main)
    else:
        await state.set_state(st.Predict.show_tournament)
        await message.answer('Выберите турнир', reply_markup =await kb.choose_tournament())


@router_user.message(st.Predict.show_tournament) 
async def choose_tournament(message: Message, state: FSMContext):
    tournament = await rq.find_tournament_by_name(message.text)
    
    if message.text != "Вернуться в меню":
        try:
            await state.set_state(st.Predict.make_predict)
            await message.answer('Кто победит в этом матче?', reply_markup =await kb.predict_match(tournament.id, 0))
        except:
            await state.clear()
            await message.answer(text = 'Турнир не найден!', reply_markup = kb.main)
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
    await message.answer("Выберите нужный топ", reply_markup = kb.rating_menu)


@router_user.message(st.ShowLeaders.show_lead) 
async def show_leaderboard_2(message: Message, state: FSMContext):
    
    if message.text == "Вернуться в меню":
        await message.answer("Меню", reply_markup = kb.main)
        await state.clear()
        return
    
    if message.text == "Рейтинги по турнирам":
        await state.set_state(st.ShowLeaders.show_tournaments)
        await message.answer("Выберите нужный топ по турниру",
                              reply_markup = await kb.show_leaderboards())
        return
    
    if message.text == "Мощнейший всеобщий топ":
        await state.clear()
        with open('tops/main_top.txt', 'r+') as f:
            text = f.read()
            await message.answer(text = text, reply_markup = kb.main)
        return
    
    await message.answer("Что-то пошло не так. Возврат в меню.", reply_markup = kb.main)
    

@router_user.message(st.ShowLeaders.show_tournaments) 
async def show_leaderboard_3(message: Message, state: FSMContext):
    await state.clear()
    try:
        name = message.text.replace(' ', '_')
        with open(f'tops/{name}_top.txt', 'r+') as f:
            text = f.read()
            await message.answer(text = text, reply_markup = kb.main)
    except:
        await message.answer("Что-то пошло не так. Возврат в меню.", reply_markup = kb.main)


@router_user.message(F.text == 'О нас')
async def show_about_us(message: Message):
    await message.answer(ABOUT_US)


@router_user.callback_query(F.data == 'Меню')
async def back_to_menu_2(callbackquery: CallbackQuery):
    await callbackquery.answer('')
    await callbackquery.message.answer("Меню", reply_markup = kb.main)


@router_user.message(F.text == 'Вернуться в меню')
async def back_to_menu_3(message: Message):
    await message.answer("Меню", reply_markup = kb.main)


@router_user.message(F.text == 'Мои предикты')
async def my_predicts(message: Message, state: FSMContext):
    await state.set_state(st.ShowPredicts.got_tournament)
    await message.answer("Выберите турнир, для которого нужно показать ваши предикты", 
                         reply_markup = await kb.ongoing_tournaments())
    

@router_user.message(st.ShowPredicts.got_tournament)
async def my_predicts(message: Message, state: FSMContext):
    await state.clear()
    if message.text == "Вернуться в меню":
        await message.answer("Меню", reply_markup = kb.main)
        return

    user_id = await rq.find_userid_by_tgid(message.from_user.id)
    matches = await rq.get_open_matches_by_tournament_name(message.text)
    text = "Ваши текущие предикты на этот турнир:\n\n"
    flag = True
    for match_ in matches:
        result = await rq.get_predict_by_ids(user_id, match_.id)
        if not result:
            continue

        winner = match_.team_1 if result == 1 else match_.team_2
        text += f"В матче {match_.team_1} vs {match_.team_2}.\nПобеда {winner}.\n\n"
        flag = False
    
    if flag:
        await message.answer("Предикты не найдены!", reply_markup = kb.main)
    else:
        await message.answer(text, reply_markup = kb.main)
