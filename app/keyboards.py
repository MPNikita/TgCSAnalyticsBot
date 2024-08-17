from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from database.data import data_tournament, data_matches


main = ReplyKeyboardMarkup(keyboard = [
    [KeyboardButton(text='Make Prediction')],
    [KeyboardButton(text='Leaderboard'), KeyboardButton(text='About Us')]
],
                                resize_keyboard=True,
                                input_field_placeholder='Choose from menu')

async def choose_tournament():
    keyboard = ReplyKeyboardBuilder()
    #request from sql server data_tournament id and name which ongoing
    for tournament in data_tournament:
        keyboard.add(KeyboardButton(text = tournament['name']))
    keyboard.adjust(2)
    keyboard.row(KeyboardButton(text = "Back to menu"))
    return keyboard.as_markup(resize_keyboard = True)


async def predict_first_match(tournament_id: int):
    keyboard = InlineKeyboardBuilder()
    #request from sql server from data_matches match by tournament_id and ongoing
    for match_it in data_matches:
        if match_it['id_tournament'] == tournament_id:
            match = match_it
            break

    match_id = match['id']
    keyboard.button(text = match['first_team'], callback_data = f'predict_{match_id}_{1}')
    keyboard.button(text = match['second_team'], callback_data = f'predict_{match_id}_{2}')
    keyboard.button(text = 'skip', callback_data = f'predict_{match_id}_{0}')
    return keyboard.adjust(2).as_markup()


async def predict_match(match_id: int):
    keyboard = InlineKeyboardBuilder()
    #request from sql server from data_matches match by tournament_id and ongoing
    #create func to find match
    flag = False
    t_id = 0
    for match_it in data_matches:
        if match_it['id'] == match_id:
            flag = True
            t_id = match_it['id_tournament']
            continue

        if flag and match_it['id_tournament'] == t_id:
            match = match_it
            break
    else:
        keyboard.button(text = 'Prediction is completed', callback_data = 'menu')
        return keyboard.as_markup()
    
    match_id = match['id']
    keyboard.button(text = match['first_team'], callback_data = f'predict_{match_id}_{1}')
    keyboard.button(text = match['second_team'], callback_data = f'predict_{match_id}_{2}')
    keyboard.button(text = 'skip', callback_data = f'predict_{match_id}_{0}')
    return keyboard.adjust(2).as_markup()
