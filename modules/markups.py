from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def markup_start():
    murkup = InlineKeyboardMarkup()
    murkup.add(InlineKeyboardButton('Что предлагает «Яблоко»', callback_data='party_program_select'))
    murkup.add(InlineKeyboardButton('Мой кандидат по округу', callback_data='z'))
    murkup.add(InlineKeyboardButton('Регистрация избирателя', callback_data='z'))
    murkup.add(InlineKeyboardButton('Я проголосовал(а)  ', callback_data='z'))
    return murkup

def markup_party_program_select():
    murkup = InlineKeyboardMarkup()
    murkup.add(InlineKeyboardButton('Федеральная часть', callback_data='party_program'))
    murkup.add(InlineKeyboardButton('Городская часть', callback_data='party_program'))
    murkup.add(InlineKeyboardButton('🔙Назад', callback_data='start'))
    return murkup