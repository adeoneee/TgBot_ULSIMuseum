from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def start_keyboard():
    buttons = [
        KeyboardButton("/start"),
        KeyboardButton("/help"),
        KeyboardButton("/submit")
    ]
    return ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons)
