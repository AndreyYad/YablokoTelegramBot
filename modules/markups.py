from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class markups():
    # Стартовое меню
    def markup_start():
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton('Что предлагает «Яблоко»', callback_data='party_program_select'),
            InlineKeyboardButton('Мой кандидат по округу', callback_data='my_candidate_address')
        )
        markup.row(
            InlineKeyboardButton('Регистрация избирателя', callback_data='want_to_registration'),
            InlineKeyboardButton('Я проголосовал(а)', callback_data='im_vote')
        )
        markup.add(InlineKeyboardButton('Техподдержка бота', url='https://t.me/sup_novgorod_yabloko_bot'))
        return markup

    # Выбор части програмы партии
    def markup_party_program_select():
        markup = InlineKeyboardMarkup()

        markup.row(
            InlineKeyboardButton('Федеральная часть', callback_data='party_program_federal'),
            InlineKeyboardButton('Городская часть', callback_data='party_program_novgorod')
        )

        markup.row(
            InlineKeyboardButton('« Назад', callback_data='start')
        )

        return markup

    # Возврат к выборы части программы партии
    def markup_party_program_back():
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('« Назад', callback_data='party_program_select'))
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
        markup.add(InlineKeyboardButton('Отмена', callback_data='start'))
        return markup
    
    # Проверка верности даных при регистрации
    def markup_check_registration_result():
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton('Да', callback_data='registration_completed'),
            InlineKeyboardButton('Нет', callback_data='registration_name')
        )
        markup.row(
            InlineKeyboardButton('Отмена регистрации', callback_data='start')
        )
        return markup
    
    # Регистрация завершена
    def markup_registration_completed():
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('Хорошо', callback_data='start'))
        return markup
    
    # Уже зарегестрирваоны
    def markup_already_registration():
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('Сменить даные', callback_data='registration_name'))
        markup.add(InlineKeyboardButton('Удалить даные', callback_data='delete_data'))
        markup.add(InlineKeyboardButton('« Назад', callback_data='start'))
        return markup
    
    # В бд есть ваш адрес
    def markup_have_address():
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton('Да', callback_data='have_address'),
            InlineKeyboardButton('Нет', callback_data='my_candidate_address_enter')
        )
        markup.row(
            InlineKeyboardButton('« Назад', callback_data='start')
        )
        return markup