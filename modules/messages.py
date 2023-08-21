TEMPLATE = {
    'address' : '''
Введите адрес регистрации по паспорту в формате: улица, дом, корпус(если есть)

Примеры:
<i>Кочетова, д. 2, корп. 2</i>
<i>Набережная Александра Невского, д. 22/2</i>
<i>проспект Мира, д. 4</i>

<u>(Ввод в неверном формате или ввод не существующего адреса приниматься не будут)</u>
'''
}

ERROR = {
    'not_format_address' : 
'''<b>Ошибка</b>: Адрес указан в не верном формате
Посмотрите примеры записи
Если вопросы остались - пишите в техподдержку(кнопка в стартовом сообщении)

<b>Ваш ввод</b>: {}
''',

    'not_found_address' : 
'''<b>Ошибка</b>: Адрес не был найден
Убедитесь, что ввели его правильно
При сохранении проблемы пишите в техподдержку(кнопка в стартовом сообщении)

<b>Ваш ввод</b>: {}
'''
}

MESSAGES = {
    'start' : '''
🍎 Этот телеграм-бот создали сторонники Новгородского отделения партии «Яблоко» с целью поддержки списка партии и кандидатов от «Яблока» на выборах депутатов Думы Великого Новгорода 10 сентября 2023 года. 

🍎 Через бот вы можете получить информацию о предвыборной программе партии и кандидатах от «Яблока», которые участвуют в выборах по вашему округу.

🍎 Зарегистрироваться избирателем «Яблока» и получить специальный значок в нашем штабе по адресу: Великий Новгород, ул. Большая Московская, дом 20/4, тел. (8162) 96-13-00.

🍎 В день голосования мы планируем провести параллельный подсчет голосов. Если Вы хотите, чтобы Ваш голос был учтен, отправьте нам фотографию бюллетеней или информацию о вашем голосовании за «Яблоко» с указанием номера избирательного участка. 
''',

    'party_program_select' : '''
Партия "ЯБЛОКО" идет на выборы депутатов Думы Великого Новгорода с программой "ЗА мир и ЗА жизнь"

Наша программа состоит из двух частей: федеральной и городской.
''',

    'party_program_federal' : '''
🕊️ <b>Немедленное заключение соглашения о прекращении огня.</b>

🍏 <i>Мир с соседями и прекращение международной изоляции России.</i>

🍏 <i>Решительная демилитаризация общества и гуманизация государственной политики.</i>

🍏 <i>Отмена цензуры, свобода собраний и свобода творчества.</i>

🍏 <i>Сменяемость власти на выборах. Отмена всех ограничений на выборах и упрощение регистрации партий и кандидатов, электронное и многодневное голосование отменяется. Строжайший контроль за честностью и прозрачностью выборов.</i>

🍏 <i>Неприкосновенность личности и частной жизни.</i>

🍏 <i>Освобождение политических заключенных.</i>

🍏 <i>Отмена репрессивного законодательства.</i>

🍏 <i>Борьба с коррупцией и полная прозрачность бюджета.</i>

🍏 <i>Развитие независимого от государственной власти местного самоуправления и гражданского общества.</i>
''',

    'party_program_novgorod' : '''
🕊️ <b>Великий Новгород для всех нас</b>

🍏 <b>Город горожан</b>
- <i>не менее 50% налогов должны оставаться в городском бюджете и расходоваться в интересах граждан</i>
- <i>строительство муниципального жилья</i>
- <i>справедливые тарифы ЖКХ</i>
- <i>современный транспорт и инфраструктура</i>

🍏 <b>Город детей</b> 
- <i>бесплатный проезд для школьников</i>
- <i>содержание детских садов и школ за счет бюджета</i>

🍏 <b>Заботливый город</b>
- <i>единый социальный проездной билет город-район для льготников</i>
- <i>повышение льготникам месячной компенсации за проезд в общественном транспорте с 300 до 600 рублей</i>
- <i>увеличение компенсаций по зубопротезированию для пожилых людей</i>

🍏 <b>Зеленый город</b>
- <i>качественное озеленение</i>
- <i>эффективная уборка улиц</i>
- <i>гуманное отношение к животным</i>

🍏 <b>Город свободы</b>
- <i>всенародные выборы мэра</i>
''',

    'already_registration' : '''
Вы уже зарегестрированы как избиратель «Яблока»

Данные, которые вы внесли:
\tИмя Фамилия : <i>{0}</i>
\tАдрес(Город, улица, дом) : <i>{1}</i> 
\tНомер телефона : <i>{2}</i> 
''',

    'want_to_registration' : '''
Вы хотите зарегистрироваться избирателем «Яблока»?
''',

    'registration_name' : '''
<b>Регистрация избирателя «Яблока»</b>

Введите имя и фамилию

<u>(Ввод в неверном формате приниматься не будет)</u>
''',

    'registration_address' : f'''
<b>Регистрация избирателя «Яблока»</b>
{TEMPLATE["address"]}
''',

    'enter_address' : f'''
{TEMPLATE["address"]}
''',

    'registration_phone' : '''
<b>Регистрация избирателя «Яблока»</b>

Введите Ваш номер телефона в формате: +79998887766

<u>(Ввод в неверном формате приниматься не будет)</u>
''',

    'check_registration_result' : '''
<b>Регистрация избирателя «Яблока»</b>

Ваши данные:
Имя Фамилия: <i>{0}</i>
Адрес: <i>{1}</i>
Номер телефона: <i>{2}</i>

<u>Всё верно?</u>
''',

    'registration_completed' : '''
Спасибо, что зарегистрировались избирателем партии «Яблоко» на выборах в Думу Великого Новгорода. Значок Вас ждет в штабе «Яблока» по адресу: Великий Новгород, ул. Большая Московская, дом 20/4, тел. (8162) 96-13-00 
''', 

    'empty_candidate' : '''
По Вашему округу партия «Яблоко» не выдвинула кандидата, но Вы можете поддержать нашу команду, проголосовав за список партии.
''',

    'candidate_info' : '''
Ваш кандидат по избирательному округу № {0} от партии «Яблоко» - <b>{2}</b>

<b>Информация о кандидате:</b>

<i>{1}</i>

''',

    'how_vote_empty' : '''
<b>Приходите на выборы в воскресенье 10 сентября 2023 года.
Голосуйте за «Яблоко» №7 в бюллетене по партийному списку.
<u>Мы не рекомендуем голосовать 8 или 9 сентября, так как Ваш голос могут украсть.</u></b>
''',

    'how_vote_cand' : '''
<b>Приходите на выборы в воскресенье 10 сентября 2023 года.
Голосуйте за «Яблоко» №7 в бюллетене по партийному списку и за нашего кандидата {} во втором бюллетене.
<u>Мы не рекомендуем голосовать 8 или 9 сентября, так как Ваш голос могут украсть.</u></b>
''',

    'candidat_stantion_info' : '''
{0}
<b>Номер вашего избирательного участка -</b> № 11{2}

<b>Адрес избирательного участка:</b>

{1}

{3}
''', 

    'have_address' : '''
Вы зарегистрировали себя как избиратель по адресу - "{}"

Использовать его?
''',

    'im_vote' : '''
Когда будут проходить выборы, зарегистрированные избиратели смогут отправить сюда фото своих бюллетений, для их сохранения.
''',

    'loading' : '''
Поиск...
''',

    'loading_excel' : '''
Обработка...
''',

    'admin_cmds' : '''
<b>Список комманд разработчика</b>

/help - <i>вывод списка команд разработчика</i>
/restart - <i>сброс состояния бота у всех пользователей</i>
/time - <i>вывод времени на сервере</i>
'''
}