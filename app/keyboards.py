from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import database.requests as rq


main = ReplyKeyboardMarkup(keyboard = [
    [KeyboardButton(text='Make Prediction')],
    [KeyboardButton(text='Leaderboard'), KeyboardButton(text='About Us')]
],
                                resize_keyboard=True,
                                input_field_placeholder='Choose from menu')

async def choose_tournament():
    keyboard = ReplyKeyboardBuilder()
    data_tournament = await rq.ongoing_tournaments()
    for tournament in data_tournament:
        keyboard.add(KeyboardButton(text = tournament.name))
    keyboard.adjust(2)
    keyboard.row(KeyboardButton(text = "Back to menu"))
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
