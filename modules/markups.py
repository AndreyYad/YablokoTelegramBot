from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class markups():
    # Стартовое меню
    def markup_start():
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('Что предлагает «Яблоко»', callback_data='party_program_select'))
        markup.add(InlineKeyboardButton('Мой кандидат по округу', callback_data='z'))
        markup.add(InlineKeyboardButton('Регистрация избирателя', callback_data='want_to_registration'))
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
    def markup_want_to_registration():
        markup = InlineKeyboardMarkup()

        markup.row(
            InlineKeyboardButton('Да', callback_data='registration_name'),
            InlineKeyboardButton('Нет', callback_data='start')
        )
        
        return markup
    
    # Отмена регистрации
    def markup_cancel():
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('Отмена', callback_data='priority_start'))
        return markup