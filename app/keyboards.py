from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
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


async def predict_match():
    keyboard = ReplyKeyboardBuilder()
    #request from sql server from data_matches match by id
    match = data_matches[0] #EXAMPLE NEED TO CHANGE
    keyboard.add(KeyboardButton(text = match['first_team']))
    keyboard.add(KeyboardButton(text = match['second_team']))
    return keyboard.adjust(2).as_markup(resize_keyboard = True)
