from aiogram import Bot
from aiogram.types import Message, InlineKeyboardMarkup, InputFile
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor, exceptions
from aiogram.bot import bot

# from os import environ

from json import load

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

import asyncio 

from datetime import datetime

from loguru import logger

from modules.markups import markups
from modules.sql_commands import sql_commands
from modules.data_commands import data
from modules.izber_parsing import izber_uchastok
from modules.logger import setup_logger

from modules.messages import MESSAGES

with open('data/okruga_data.json', encoding='utf-8') as file:
    OKRUGA = load(file)

with open('data/stations_data.json', encoding='utf-8') as file:
    STATIONS_DESC = load(file)

with open('config.json') as file:
    config = load(file)
    TOKEN = config['token']
    ADMIN_ID = config['admins_id']
    VIP_USER_ID = config['vip_id']

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

lamb_izber_uchastok = lambda address: izber_uchastok(address['street'], '{} {}'.format(address['house'], address['korp']))

setup_logger()

logger.info("Бот запущен")

# print('Бот запущен')

# Информация о кандите округа и о избирательном участке
async def send_info_okrug(user_id, station_num):
        okrug_info = [okrug for okrug in OKRUGA if station_num in okrug['stations']][0]
        if okrug_info['name'] == '':
            okrug_info_text = MESSAGES['empty_candidate']
            how_vote_text = MESSAGES['how_vote_empty']
            photo = None
        else:
            okrug_info_text = MESSAGES['candidate_info'].format(okrug_info['num'], okrug_info['description'], okrug_info['name'])
            how_vote_text = MESSAGES['how_vote_cand'].format(okrug_info['name_vin'])
            photo = open('img/{}.jpg'.format(okrug_info['num']), 'rb')
            await send_msg(user_id, photo=photo)
        await send_msg(
            user_id,
            MESSAGES['candidat_stantion_info'].format(
                okrug_info_text, 
                STATIONS_DESC[station_num-1], 
                str(station_num).zfill(2), 
                how_vote_text
            ),
            markup=markups.markup_registration_completed(),
            delete=(photo == None)
        )

async def delete_msg_bot(id):
    for msg_id in sql_commands.history_bot_msg(id):
        try:
            await bot.delete_message(id, msg_id)
        except exceptions.MessageToDeleteNotFound:
            pass
        sql_commands.clear_history_bot_msg(msg_id)

async def send_msg(id, text='', markup=InlineKeyboardMarkup(), delete=True, photo=None, document=None):
    if document != None:
        msg_id = (await bot.send_document(chat_id=id, document=document, reply_markup=markup)).message_id
    elif photo != None:
        msg_id = (await bot.send_photo(chat_id=id, photo=photo)).message_id
    else:
        msg_id = (await bot.send_message(id, text, reply_markup=markup, parse_mode='html')).message_id
    if delete:
        await delete_msg_bot(id)
    sql_commands.change_in_table('bot', 'INSERT OR IGNORE INTO bot_msg VALUES (\'%d\', \'%d\')' % (msg_id, id))

async def daily_reset():
    for id_ in sql_commands.grab_users_id():
        await delete_msg_bot(id_)
        sql_commands.set_status(id_, 'none')
    logger.info(f"сброс (запланированный)")

async def scheduler():
    scheduler = AsyncIOScheduler()
    time_trigger = CronTrigger(hour='7', minute='30')
    scheduler.add_job(daily_reset, time_trigger)
    scheduler.start()


@dp.message_handler(commands = ['start'])
async def start_func(msg: Message, send=True):

    sql_commands.change_in_table('bot', 'INSERT OR IGNORE INTO users VALUES (\'%d\', \'none\')' % (msg.chat.id))

    data.delete_pre_reg(msg.chat.id)
    sql_commands.set_status(msg.chat.id, 'none')

    if send:
        await send_msg(msg.chat.id, MESSAGES['start'], markup=markups.markup_start(msg.chat.id in VIP_USER_ID))

    await bot.delete_message(msg.chat.id, msg.message_id)

    logger.info(f"{msg.chat.id}: команда /start")

@dp.message_handler()
async def enter_start(msg: Message):

    edit = lambda text, markup: bot.edit_message_text(
        text, 
        msg.chat.id, 
        sql_commands.history_bot_msg(msg.chat.id)[-1], 
        reply_markup=markup, 
        parse_mode='html'
    )

    status = sql_commands.check_status(msg.chat.id)

    await bot.delete_message(msg.from_user.id, msg.message_id)

    # Для админа
    if msg.chat.id in ADMIN_ID:

        if msg.text == '/help':
            await send_msg(msg.from_user.id, MESSAGES['admin_cmds'])
            sql_commands.set_status(msg.chat.id, 'none')

        if msg.text == '/restart':
            for id_ in sql_commands.grab_users_id():
                await delete_msg_bot(id_)
                sql_commands.set_status(msg.chat.id, 'none')
            logger.info(f"сброс (команда)")

        if msg.text == '/time':
            await send_msg(msg.from_user.id, datetime.now(), delete=False)

    #Для народа
    if status == 'reg_name':
        if len(msg.text.split(' ')) == 2 and msg.text.replace(' ','f').isalpha():
            sql_commands.change_in_table('bot', 'INSERT OR IGNORE INTO pre_reg (id, name) VALUES (\'%d\', \'%s\')' % (msg.chat.id, msg.text))
            await edit(MESSAGES['registration_address'], markups.markup_cancel())
            sql_commands.set_status(msg.chat.id, 'reg_address')
            logger.info(f"{msg.chat.id}: имя фамилия заполнены ({msg.text})")
        else:
            logger.warning(f"{msg.chat.id}: имя фамилия не верного формата ({msg.text})")

    elif status in ['reg_address', 'my_cand_addres']:
        
        address = data.text_to_address(msg.text)
        # print(address)

        if address != None:

            station_num = await lamb_izber_uchastok(address)

            if station_num != None:

                text = msg.text.lower().split(',')
                text[0] = text[0].title()
                text = ','.join(text)

                sql_commands.change_in_table('bot', 'INSERT OR IGNORE INTO pre_reg (id) VALUES (\'%d\')' % (msg.chat.id))
                sql_commands.change_in_table('bot', 'UPDATE pre_reg SET address = \'%s\' WHERE id = \'%d\'' % (text, msg.chat.id))
                user_info = sql_commands.grab_pre_reg_data(msg.chat.id)

                if status == 'reg_address':
                    await edit(MESSAGES['registration_phone'], markups.markup_cancel())
                    sql_commands.set_status(msg.chat.id, 'reg_phone')
                    logger.info(f"{msg.chat.id}: адрес зарегистрирован ({text})")
                elif status == 'my_cand_addres':
                    await bot.edit_message_text(
                        MESSAGES['loading'], 
                        msg.chat.id, 
                        sql_commands.history_bot_msg(msg.chat.id)[0], 
                        parse_mode='html'
                    )
                    sql_commands.set_status(msg.chat.id, 'none')
                    await send_info_okrug(msg.chat.id, station_num)
                    logger.info(f"{msg.chat.id}: участок и округ определены ({text})")

            else:
                logger.warning(f"{msg.chat.id}: адрес не определён ({msg.text})")

        else:
            logger.warning(f"{msg.chat.id}: адрес не верного формата ({msg.text})")

    
    elif status == 'reg_phone':
        if len(msg.text) == 12 and msg.text.startswith('+7') and msg.text[2:].isdigit():
            sql_commands.change_in_table('bot', 'UPDATE pre_reg SET phone = \'%s\' WHERE id = \'%d\'' % (msg.text, msg.chat.id))
            sql_commands.set_status(msg.chat.id, 'none')
            user_info = sql_commands.grab_pre_reg_data(msg.chat.id)
            await edit(
                MESSAGES['check_registration_result'].format(user_info[0], user_info[1], user_info[2]), 
                markups.markup_check_registration_result()
            )
            logger.info(f"{msg.chat.id}: телефон зарегистрирован ({msg.text})")
        else:
            logger.warning(f"{msg.chat.id}: телефон не верного формата ({msg.text})")

# Удаление лишних сообщений (Фото, видео, стикеры и др.)
@dp.message_handler(content_types = ['any'])
async def delete_other_func(msg: Message):
    await bot.delete_message(msg.from_user.id, msg.message_id)

@dp.callback_query_handler()
async def callback(call):

    user_id = call.message.chat.id
    edit = lambda text, markup=InlineKeyboardMarkup(): bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup, parse_mode='html')
    
    if call.data == 'delete_data':
        data.delete_voter_data(user_id)
        logger.info(f"{user_id}: данные регистрации удалены")

    try:
        if call.data in ['start', 'delete_data']:
            data.delete_pre_reg(user_id)
            sql_commands.set_status(user_id, 'none')
            if len(sql_commands.history_bot_msg(user_id)) == 2:
                try:
                    msg_photo_id = sql_commands.history_bot_msg(user_id)[0]
                    await bot.delete_message(user_id, msg_photo_id)
                    sql_commands.clear_history_bot_msg(msg_photo_id)
                except exceptions.MessageToDeleteNotFound:
                    pass
            try:
                await edit(MESSAGES['start'], markups.markup_start(user_id in VIP_USER_ID))
            except exceptions.BadRequest:
                await send_msg(user_id, MESSAGES['start'], markup=markups.markup_start(user_id in VIP_USER_ID))
        
        elif call.data == 'party_program_select':
            await edit(MESSAGES['party_program_select'], markups.markup_party_program_select())

        elif call.data == 'party_program_federal':
            await edit(MESSAGES['party_program_federal'], markups.markup_party_program_back())

        elif call.data == 'party_program_novgorod':
            await edit(MESSAGES['party_program_novgorod'], markups.markup_party_program_back())

        elif call.data == 'want_to_registration':
            voter_data = sql_commands.grab_registration_data(user_id)
            if voter_data == None:
                await edit(MESSAGES['want_to_registration'], markups.markup_want_to_registration())
            else:
                await edit(MESSAGES['already_registration'].format(voter_data[0], voter_data[1], voter_data[2]), markups.markup_already_registration())

        elif call.data == 'registration_name':
            data.delete_pre_reg(user_id)
            sql_commands.set_status(user_id, 'reg_name')
            await edit(MESSAGES['registration_name'], markups.markup_cancel())
            logger.info(f"{user_id}: начало регистрации")

        elif call.data == 'registration_completed':
            voter_data = sql_commands.grab_pre_reg_data(user_id)
            sql_commands.change_in_table('yabloko', 'INSERT OR IGNORE INTO voters (id) VALUES (\'%d\')' % (user_id))
            sql_commands.change_in_table(
                'yabloko', 
                'UPDATE voters SET name = \'%s\', address = \'%s\', phone = \'%s\' WHERE id = \'%d\'' % (voter_data[0], voter_data[1], voter_data[2], user_id)
            )
            data.delete_pre_reg(user_id)
            sql_commands.set_status(user_id, 'none')
            await edit(MESSAGES['registration_completed'], markups.markup_registration_completed())
            logger.info(f"{user_id}: регистрация пройдена")

        elif call.data.startswith('my_candidate_address'):
            if sql_commands.check_registration(user_id) and call.data == 'my_candidate_address':
                await edit(MESSAGES['have_address'].format(sql_commands.grab_registration_data(user_id)[1]), markups.markup_have_address())
            else:
                sql_commands.set_status(user_id, 'my_cand_addres')
                await edit(MESSAGES['enter_address'], markups.markup_cancel())

        elif call.data == 'have_address':
            await edit(MESSAGES['loading'])
            addres_orig = sql_commands.grab_registration_data(user_id)[1]
            address = data.text_to_address(addres_orig)
            station_num = await lamb_izber_uchastok(address)
            await send_info_okrug(user_id, station_num)
            logger.info(f"{user_id}: участок и округ определены ({addres_orig})")

        elif call.data == 'im_vote':
            await edit(MESSAGES['im_vote'], markups.markup_registration_completed())

        elif call.data == 'get_excel':
            await edit(MESSAGES['loading_excel'])
            await send_msg(user_id, markup=markups.markup_back_to_start(), document=data.get_excel())
            logger.info(f"{user_id}: выдача файла таблицы")

    except exceptions.MessageNotModified:
        pass

if __name__ == '__main__':
    data.born_of_tables()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(scheduler())

    executor.start_polling(dp, loop=loop)