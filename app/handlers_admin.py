from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from app.config import ADMINS
from aiogram.fsm.context import FSMContext 
import database.requests as rq
import app.keyboards as kb
import app.states as st
import utils.funcs as ufuncs



router_admin = Router()


async def admin_checker(id):
    if id in ADMINS:
        return True
    return False


@router_admin.message(Command('create_tournament'))
async def create_tournament_1(message: Message, state: FSMContext):
    if not await admin_checker(message.from_user.id):
        await message.answer('No permission')
        return
    
    await state.set_state(st.TournamentCreation.name)
    await message.answer('Введите название турнира. Внимание, название турнира должно в точности повторять название турнира с hltv.org !!!')


@router_admin.message(st.TournamentCreation.name)
async def create_tournament_2(message: Message, state: FSMContext):
    await state.clear()
    name = message.text
    name = name.replace(' ', '_')
    with open(f'tops/{name}_top.txt', 'w+') as f:
        f.write('Данный турнир ещё не начался.')
    await message.answer(text = await rq.new_tournament(message.text))


@router_admin.message(Command('create_match'))
async def create_match_1(message: Message, state: FSMContext):
    if not await admin_checker(message.from_user.id):
        await message.answer('Нет доступа')
        return
    
    await state.set_state(st.MatchCreation.team1)
    await message.answer('Введите название турнира. Внимание, название турнира должно в точности повторять название турнира с hltv.org !!!')


@router_admin.message(st.MatchCreation.team1)
async def create_match_2(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await state.set_state(st.MatchCreation.team2)
    await message.answer(text = "Введите название первой команды, строго как на hltv.org !")


@router_admin.message(st.MatchCreation.team2)
async def create_match_3(message: Message, state: FSMContext):
    await state.update_data(team1 = message.text)
    await state.set_state(st.MatchCreation.creation)
    await message.answer(text = "Введите название второй команды, строго как на hltv.org !")


@router_admin.message(st.MatchCreation.creation)
async def create_match_4(message: Message, state: FSMContext):
    await state.update_data(team2 = message.text)
    data = await state.get_data()
    await state.clear()
    await message.answer(text = await rq.new_match(data['name'], data['team1'],data['team2']))


@router_admin.message(Command('open_predicts'))
async def open_1(message: Message, state: FSMContext):
    if not await admin_checker(message.from_user.id):
        await message.answer('Нет доступа')
        return
    
    await state.set_state(st.OpenPredicts.open_)
    await message.answer("Прогнозы на какой турнир открыть?", reply_markup = await kb.open_tournament())


@router_admin.message(st.OpenPredicts.open_)
async def open_2(message: Message, state: FSMContext):
    await rq.open_tournament(message.text)
    await message.answer(text = f"Прогнозы на {message.text} открыты!")


@router_admin.message(Command('close_predicts'))
async def close_1(message: Message, state: FSMContext):
    if not await admin_checker(message.from_user.id):
        await message.answer('Нет доступа')
        return
    
    await state.set_state(st.ClosePredicts.close_)
    await message.answer("Прогнозы на какой турнир закрыть?", reply_markup = await kb.close_tournament())


@router_admin.message(st.ClosePredicts.close_)
async def close_2(message: Message, state: FSMContext):
    await rq.close_tournament(message.text)
    await message.answer(text = f"Прогнозы на {message.text} закрыты!")


@router_admin.message(Command('match_stats'))
async def match_stats_1(message: Message, state: FSMContext):
    if not await admin_checker(message.from_user.id):
        await message.answer('No permission')
        return

    await state.set_state(st.MatchStats.stats)
    await message.answer(text = "Выберите матч для предоставления статистики!", 
                         reply_markup = await kb.open_matches())


@router_admin.message(st.MatchStats.stats)
async def match_stats_2(message: Message, state: FSMContext):
    await state.clear()
    id_str, teams = message.text.split(';')
    team1, team2 = teams.split(' vs ')
    _, match_id = id_str.split(': ')
    predicts = list(await rq.get_match_pred(int(match_id)))
    stats = [0, len(predicts)]
    for pred in predicts:
        if pred.result == 1:
            stats[0] += 1
    wr_1 = stats[0] / stats[1] * 100
    await message.answer(text = f"Сделано прогнозов: {stats[1]}\nПредсказали победу {team1}: {stats[0]} {wr_1:.2f}%\nПредсказали победу {team2}: {stats[1] -stats[0]} {100 - wr_1:.2f}%", 
                         reply_markup = ReplyKeyboardRemove())


@router_admin.message(Command('update_match'))
async def update_match_1(message: Message, state: FSMContext):
    if not await admin_checker(message.from_user.id):
        await message.answer('No permission')
        return

    await state.set_state(st.MatchUpdate.show_stats)
    await message.answer(text = "Выберите матч для внесение результатов ", 
                         reply_markup = await kb.open_matches())


@router_admin.message(st.MatchUpdate.show_stats)
async def update_match_2(message: Message, state: FSMContext):
    await state.set_state(st.MatchUpdate.match_upd)
    id_str, teams = message.text.split(';')
    team1, team2 = teams.split(' vs ')
    _, match_id = id_str.split(': ')
    predicts = list(await rq.get_match_pred(int(match_id)))
    stats = [0, len(predicts)]
    for pred in predicts:
        if pred.result == 1:
            stats[0] += 1
    wr_1 = stats[0] / stats[1] * 100
    await message.answer(text = f"Сделано прогнозов: {stats[1]}\nПредсказали победу {team1}: {stats[0]} {wr_1:.2f}%\nПредсказали победу {team2}: {stats[1] -stats[0]} {100 - wr_1:.2f}%", 
                         reply_markup = await kb.choose_result(int(match_id), team1, team2))


@router_admin.message(st.MatchUpdate.match_upd)
async def update_match_3(message: Message, state: FSMContext):
    await state.clear()
    _, id_str, result = message.text.split('; ')
    _, match_id = id_str.split(':')
    await rq.update_match(int(match_id), int(result))
    await ufuncs.update_text_tops(int(match_id))
    await message.answer(text = f'Матч обновлен.\nMatch id: {match_id} result: {result}',
                         reply_markup = ReplyKeyboardRemove())
    

@router_admin.message(Command('broadcast_message'))
async def broadcast_message_1(message: Message, state: FSMContext):
    if not await admin_checker(message.from_user.id):
        await message.answer('No permission')
        return
    
    await state.set_state(st.Broadcast.got_msg)
    await message.answer(text = "Пожалуйста, введите текст сообщения, которое хотите всем отправить")


@router_admin.message(st.Broadcast.got_msg)
async def broadcast_message_2(message: Message, state: FSMContext):
    await state.update_data(got_msg = message.text)
    await state.set_state(st.Broadcast.confirm)
    await message.answer(text = message.text)
    await message.answer(text = "Проверьте сообщение и подтвердите отправку", 
                         reply_markup = kb.confirmation)
    

@router_admin.message(st.Broadcast.confirm)
async def broadcast_message_3(message: Message, state: FSMContext):
    if message.text == 'Отмена':
        await message.answer(text = "Текст не отправлен", 
                         reply_markup = ReplyKeyboardRemove())
        await state.clear()

    data = await state.get_data()
    users = await rq.get_users_id()
    await message.answer(text = "Начинается рассылка!")
    await state.clear()
    for user in users:
        try:
            await message.bot.send_message(user, text = data['got_msg'])
        except:
            pass
    await message.answer(text = "Текст отправлен!", 
                         reply_markup = ReplyKeyboardRemove())


@router_admin.message(Command('admin'))
async def admin_commands(message: Message):
    if not await admin_checker(message.from_user.id):
        await message.answer('No permission')
        return
    
    await message.answer(text = "Привет Админ!", 
                         reply_markup = kb.admin_panel)
    

@router_admin.message(Command('new_predict'))
async def make_predict_1(message: Message, state: FSMContext):
    if not await admin_checker(message.from_user.id):
        await message.answer('No permission')
        return
    
    await state.set_state(st.AdminMakePredict.tournament_name)
    await message.answer(text = 'Выберите турнир, на который вы хотите ввести предикты',
                         reply_markup = await kb.all_touranments_admin())
    

@router_admin.message(st.AdminMakePredict.tournament_name)
async def make_predict_2(message: Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.clear()
        await message.answer(text = 'Действие отменено', reply_markup = ReplyKeyboardRemove())
        return
    
    await state.update_data(tournament_name = message.text)
    await state.set_state(st.AdminMakePredict.making)
    await message.answer(text = 'Введите предикт игрока формата:\nusername,predict,team1,team2,result\nВСЕ БЕЗ ПРОБЕЛОВ\nПока вы не нажмете кнопку отмена продолжайте присылать предикты, после подтверждения получения!\nЛишний раз не используйте эту команду!', 
                         reply_markup = kb.cancel)
    

@router_admin.message(st.AdminMakePredict.making)
async def make_predict_3(message: Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.clear()
        await message.answer(text = 'Прием предиктов остановлен! Команда завершена!', 
                             reply_markup = ReplyKeyboardRemove())
        return
    
    data_from_state = await state.get_data()
    username, predict, team1, team2, result = message.text.split(',')
    await message.answer(text = await rq.new_predict_admin(data_from_state['tournament_name'], username, predict, team1, team2, result))
