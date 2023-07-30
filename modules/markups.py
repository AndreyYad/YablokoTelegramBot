from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def markup_start():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Что предлагает «Яблоко»', callback_data='party_program_select'))
    markup.add(InlineKeyboardButton('Мой кандидат по округу', callback_data='z'))
    markup.add(InlineKeyboardButton('Регистрация избирателя', callback_data='z'))
    markup.add(InlineKeyboardButton('Я проголосовал(а)  ', callback_data='z'))
    return markup

def markup_party_program_select():
    markup = InlineKeyboardMarkup()

    btn1 = InlineKeyboardButton('Федеральная часть', callback_data='party_program')
    btn2 = InlineKeyboardButton('Городская часть', callback_data='party_program')
    btn3 = InlineKeyboardButton('🔙Назад', callback_data='start')

    

    markup.add(InlineKeyboardButton('Федеральная часть', callback_data='party_program'))
    markup.add(InlineKeyboardButton('Городская часть', callback_data='party_program'))
    markup.add(InlineKeyboardButton('🔙Назад', callback_data='start'))
    return markup

def markup_party_program_open():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('🔙Назад', callback_data='party_program'))