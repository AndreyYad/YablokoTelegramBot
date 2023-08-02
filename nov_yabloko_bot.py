from aiogram import Bot
from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor, exceptions
from aiogram.bot import bot

from os import environ

from modules.messages import MESSAGES

from modules.markups import markups
from modules.sql_commands import sql_commands

bot = Bot(token=environ['TELEGRAM_BOT_TOKEN'])
dp = Dispatcher(bot)

async def delete_msg_bot(id):
    for msg_id in sql_commands.history_bot_msg(id):
        try:
            await bot.delete_message(id, msg_id)
        except exceptions.MessageToDeleteNotFound:
            pass
        sql_commands.clear_history_bot_msg(msg_id)

async def send_msg(id, text, markup=InlineKeyboardMarkup()):
    await delete_msg_bot(id)
    msg_id = (await bot.send_message(id, text, reply_markup=markup)).message_id
    sql_commands.change_in_table('bot', 'INSERT OR IGNORE INTO bot_msg VALUES (\'%d\', \'%d\')' % (msg_id, id))

@dp.message_handler(commands = ['start'])
async def start_func(msg: Message):

    sql_commands.born_of_tables()

    sql_commands.change_in_table('bot', 'INSERT OR IGNORE INTO users VALUES (\'%d\', \'none\')' % (msg.chat.id))

    if sql_commands.check_status(msg.chat.id) != 'none':
        sql_commands.set_status(msg.chat.id, 'none')
        sql_commands.change_in_table('bot', 'DELETE FROM pre_reg WHERE id == \'%d\'' % (msg.chat.id))

    await send_msg(msg.from_user.id, MESSAGES['start'], markup=markups.markup_start())

    await bot.delete_message(msg.from_user.id, msg.message_id)

@dp.message_handler()
async def enter_start(msg: Message):

    status = sql_commands.check_status(msg.chat.id)
    
    if status == 'reg_name' and len(msg.text.split(' ')) == 2 and msg.text.replace(' ','f').isalpha():
        sql_commands.change_in_table('bot', 'INSERT OR IGNORE INTO pre_reg (id, name) VALUES (\'%d\', \'%s\')' % (msg.chat.id, msg.text))
        await send_msg(msg.chat.id, MESSAGES['registration_address'])
        sql_commands.set_status(msg.chat.id, 'reg_address')
    elif status == 'reg_address':
        sql_commands.change_in_table('bot', 'UPDATE pre_reg SET address = \'%s\' WHERE id = \'%d\'' % (msg.text, msg.chat.id))

    await bot.delete_message(msg.from_user.id, msg.message_id)

@dp.callback_query_handler()
async def callback(call):

    user_id = call.message.chat.id
    edit = lambda text, markup: bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)
    
    if call.data == 'start':
        await edit(MESSAGES['start'], markups.markup_start())
    
    elif call.data == 'party_program_select':
        await edit(MESSAGES['party_program_select'], markups.markup_party_program_select())

    elif call.data == 'party_program_federal':
        await edit(MESSAGES['party_program_federal'], markups.markup_party_program_back())

    elif call.data == 'party_program_novgorod':
        await edit(MESSAGES['party_program_novgorod'], markups.markup_party_program_back())

    elif call.data == 'want_to_registration':
        await edit(MESSAGES['want_to_registration'], markups.markup_want_to_registration())

    elif call.data == 'registration_name':
        sql_commands.set_status(user_id, 'reg_name')
        await send_msg(user_id, MESSAGES['registration_name'])


if __name__ == '__main__':
    executor.start_polling(dp)