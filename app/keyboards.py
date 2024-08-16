from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


main = ReplyKeyboardMarkup(keyboard = [
    [KeyboardButton(text='Make Prediction')],
    [KeyboardButton(text='Leaderboard'), KeyboardButton(text='About Us')]
],
                                resize_keyboard=True,
                                input_field_placeholder='Choose from menu')