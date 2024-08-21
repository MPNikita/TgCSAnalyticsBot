from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import database.requests as rq


main = ReplyKeyboardMarkup(keyboard = [
    [KeyboardButton(text='Провести мощнейшую аналитику')],
    [KeyboardButton(text='Рейтинг аналитиков'), KeyboardButton(text='О нас')]
],
                                resize_keyboard=True,
                                input_field_placeholder='Выберите один из пунктов')


async def choose_tournament():
    keyboard = ReplyKeyboardBuilder()
    data_tournament = await rq.opened_tournaments()
    for tournament in data_tournament:
        keyboard.add(KeyboardButton(text = tournament.name))
    keyboard.adjust(2)
    keyboard.row(KeyboardButton(text = "Вернуться в меню"))
    return keyboard.as_markup(resize_keyboard = True)


async def predict_match(tournament_id, match_local_id):
    keyboard = InlineKeyboardBuilder()
    matches = list(await rq.matches_to_predict(tournament_id))

    if len(matches) == match_local_id + 1:
        exists_next = 'no'
    else:
        exists_next = 'yes'

    local_match = matches[match_local_id]
    
    keyboard.button(text = local_match.team_1, callback_data = f'predict_{local_match.id}_{tournament_id}_{match_local_id}_{1}_{exists_next}')
    keyboard.button(text = local_match.team_2, callback_data = f'predict_{local_match.id}_{tournament_id}_{match_local_id}_{2}_{exists_next}')
    return keyboard.adjust(2).as_markup()


async def open_tournament():
    keyboard = ReplyKeyboardBuilder()
    data_tournament = await rq.closed_tournaments()
    for tournament in data_tournament:
        keyboard.add(KeyboardButton(text = tournament.name))
    keyboard.adjust(1)
    return keyboard.as_markup(resize_keyboard = True)


async def close_tournament():
    keyboard = ReplyKeyboardBuilder()
    data_tournament = await rq.opened_tournaments()
    for tournament in data_tournament:
        keyboard.add(KeyboardButton(text = tournament.name))
    keyboard.adjust(1)
    return keyboard.as_markup(resize_keyboard = True)


async def open_matches():
    keyboard = ReplyKeyboardBuilder()
    opened_matches = await rq.opened_matches()
    for match_ in opened_matches:
        keyboard.add(KeyboardButton(text = f'id: {match_.id};{match_.team_1} vs {match_.team_2}'))
    keyboard.adjust(1)
    return keyboard.as_markup(resize_keyboard = True)


async def choose_result(id, team1, team2):
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text = f'Выиграли {team1}; id:{id}; 1'))
    keyboard.add(KeyboardButton(text = f'Выиграли {team2}; id:{id}; 2'))
    keyboard.adjust(1)
    return keyboard.as_markup(resize_keyboard = True)


async def show_leaderboards():
    keyboard = ReplyKeyboardBuilder()
    tournaments = await rq.get_tournaments()
    keyboard.add(KeyboardButton(text = "Мощнейший всеобщий топ"))
    for tournament in tournaments:
        keyboard.add(KeyboardButton(text = tournament.name))
    keyboard.adjust(1)
    return keyboard.as_markup(resize_keyboard = True)
