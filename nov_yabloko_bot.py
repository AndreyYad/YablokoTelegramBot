from aiogram import Bot
from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor, exceptions
from aiogram.bot import bot

from os import environ

from json import load

from modules.markups import markups
from modules.sql_commands import sql_commands
from modules.data_commands import data
from modules.izber_parsing import izber_uchastok

from modules.messages import MESSAGES

with open('data/okruga_data.json', encoding='utf-8') as file:
    OKRUGA = load(file)

bot = Bot(token=environ['TELEGRAM_BOT_TOKEN'])
dp = Dispatcher(bot)

lamb_izber_uchastok = lambda address: izber_uchastok(address['street'], '{} {}'.format(address['house'], address['korp']))

print('Бот запущен')

# Информация о кандите округа и о избирательном участке
async def send_info_okrug(user_id, uchastok_info):
        okrug_info = [okrug for okrug in OKRUGA if uchastok_info['num'] in okrug['stations']][0]
        if okrug_info['candidat'] == '':
            okrug_info_text = MESSAGES['empty_candidate']
        else:
            okrug_info_text = MESSAGES['candidate_info'].format(okrug_info['num'], okrug_info['candidat'])
        await send_msg(
            user_id,
            MESSAGES['candidat_stantion_info'].format(okrug_info_text, uchastok_info['address'], str(uchastok_info['num']).zfill(2)),
            markup=markups.markup_registration_completed()
        )

async def delete_msg_bot(id):
    for msg_id in sql_commands.history_bot_msg(id):
        try:
            await bot.delete_message(id, msg_id)
        except exceptions.MessageToDeleteNotFound:
            pass
        sql_commands.clear_history_bot_msg(msg_id)

async def send_msg(id, text, markup=InlineKeyboardMarkup(), delete=True):
    if delete:
        await delete_msg_bot(id)
    msg_id = (await bot.send_message(id, text, reply_markup=markup, parse_mode='html')).message_id
    sql_commands.change_in_table('bot', 'INSERT OR IGNORE INTO bot_msg VALUES (\'%d\', \'%d\')' % (msg_id, id))

@dp.message_handler(commands = ['start'])
async def start_func(msg: Message, send=True):

    sql_commands.change_in_table('bot', 'INSERT OR IGNORE INTO users VALUES (\'%d\', \'none\')' % (msg.chat.id))

    data.delete_pre_reg(msg.chat.id)
    sql_commands.set_status(msg.chat.id, 'none')

    if send:
        await send_msg(msg.from_user.id, MESSAGES['start'], markup=markups.markup_start())

    await bot.delete_message(msg.from_user.id, msg.message_id)

@dp.message_handler()
async def enter_start(msg: Message):

    status = sql_commands.check_status(msg.chat.id)
    
    if status == 'reg_name' and len(msg.text.split(' ')) == 2 and msg.text.replace(' ','f').isalpha():
        sql_commands.change_in_table('bot', 'INSERT OR IGNORE INTO pre_reg (id, name) VALUES (\'%d\', \'%s\')' % (msg.chat.id, msg.text))
        await send_msg(msg.chat.id, MESSAGES['registration_address'], markup=markups.markup_cancel())
        sql_commands.set_status(msg.chat.id, 'reg_address')

    elif status in ['reg_address', 'my_cand_addres']:
        
        address = data.text_to_address(msg.text)
        print(address)

        if address != None:

            info_okrug = await lamb_izber_uchastok(address)

            if info_okrug != None:

                sql_commands.change_in_table('bot', 'INSERT OR IGNORE INTO pre_reg (id) VALUES (\'%d\')' % (msg.chat.id))
                sql_commands.change_in_table('bot', 'UPDATE pre_reg SET address = \'%s\' WHERE id = \'%d\'' % (msg.text, msg.chat.id))
                user_info = sql_commands.grab_pre_reg_data(msg.chat.id)

                if status == 'reg_address':
                    await send_msg(msg.chat.id, MESSAGES['registration_phone'], markup=markups.markup_cancel())
                    sql_commands.set_status(msg.chat.id, 'reg_phone')
                elif status == 'my_cand_addres':
                    sql_commands.set_status(msg.chat.id, 'none')
                    await send_info_okrug(msg.chat.id, info_okrug)
    
    elif status == 'reg_phone' and len(msg.text) == 12 and msg.text.startswith('+7') and msg.text[2:].isdigit():
        sql_commands.change_in_table('bot', 'UPDATE pre_reg SET phone = \'%s\' WHERE id = \'%d\'' % (msg.text, msg.chat.id))
        sql_commands.set_status(msg.chat.id, 'none')
        user_info = sql_commands.grab_pre_reg_data(msg.chat.id)
        await send_msg(
            msg.chat.id, 
            MESSAGES['check_registration_result'].format(user_info[0], user_info[1], user_info[2]), 
            markup=markups.markup_check_registration_result()
        )
        
    await bot.delete_message(msg.from_user.id, msg.message_id)

@dp.callback_query_handler()
async def callback(call):

    user_id = call.message.chat.id
    edit = lambda text, markup: bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup, parse_mode='html')
    
    if call.data == 'delete_data':
        data.delete_voter_data(user_id)

    try:
        if call.data in ['start', 'delete_data']:
            data.delete_pre_reg(user_id)
            sql_commands.set_status(user_id, 'none')
            await edit(MESSAGES['start'], markups.markup_start())
        
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

        elif call.data.startswith('my_candidate_address'):
            if sql_commands.check_registration(user_id) and call.data == 'my_candidate_address':
                await edit(MESSAGES['have_address'].format(sql_commands.grab_registration_data(user_id)[1]), markups.markup_have_address())
            else:
                sql_commands.set_status(user_id, 'my_cand_addres')
                await edit(MESSAGES['enter_address'], markups.markup_cancel())

        elif call.data == 'have_address':
            address = data.text_to_address(sql_commands.grab_registration_data(user_id)[1])
            info_okrug = await lamb_izber_uchastok(address)
            await send_info_okrug(user_id, info_okrug)

        elif call.data == 'im_vote':
            await edit(MESSAGES['im_vote'], markups.markup_registration_completed())

    except exceptions.MessageNotModified:
        pass

if __name__ == '__main__':
    data.born_of_tables()
    executor.start_polling(dp)