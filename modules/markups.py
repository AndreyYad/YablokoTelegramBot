from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class markups():
    # Стартовое меню
    def markup_start():
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('Что предлагает «Яблоко»', callback_data='party_program_select'))
        markup.add(InlineKeyboardButton('Мой кандидат по округу', callback_data='z'))
        markup.add(InlineKeyboardButton('Регистрация избирателя', callback_data='z'))
        markup.add(InlineKeyboardButton('Я проголосовал(а)  ', callback_data='z'))
        return markup

    # Выбор части програмы партии
    def markup_party_program_select():
        markup = InlineKeyboardMarkup()

        markup.row(
            InlineKeyboardButton('Федеральная часть', callback_data='party_program_federal'),
            InlineKeyboardButton('Городская часть', callback_data='party_program_novgorod')
        )

        markup.row(
            InlineKeyboardButton('🔙Назад', callback_data='start')
        )

        return markup

    # Возврат к выборы части программы партии
    def markup_party_program_back():
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('🔙Назад', callback_data='party_program_select'))
        return markup
    
    # Начало регистрации