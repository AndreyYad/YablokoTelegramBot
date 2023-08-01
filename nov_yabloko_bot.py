from aiogram import Bot
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor, exceptions
from aiogram.bot import bot

from sqlite3 import connect

from modules.config import TOKEN
from modules.messages import MESSAGES

from modules.markups import markups
from modules.sql_commands import sql_commands

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands = ['start'])
async def start_func(msg: Message):

    sql_commands.change_in_table('bot', 'CREATE TABLE IF NOT EXISTS users (id int primary key, status varchar(50))')
    sql_commands.change_in_table('bot', 'CREATE TABLE IF NOT EXISTS bot_msg (msg_id int primary key, user_id int)')
    sql_commands.change_in_table('yabloko', 'CREATE TABLE IF NOT EXISTS voters (id int primary key, name varchar(50), address varchar(100))')
    sql_commands.change_in_table('bot', 'CREATE TABLE IF NOT EXISTS pre_reg (id int primary key, name varchar(50), address varchar(100))')

    sql_commands.change_in_table('bot', 'INSERT OR IGNORE INTO users VALUES (\'%d\', \'none\')' % (msg.chat.id))

    if sql_commands.check_status(msg.chat.id) != 'none':
        sql_commands.set_status(msg.chat.id, 'none')
        sql_commands.change_in_table('bot', 'DELETE FROM pre_reg WHERE id == \'%d\'' % (msg.chat.id))

    await bot.send_message(msg.from_user.id, MESSAGES['start'], reply_markup=markups.markup_start())
    await bot.delete_message(msg.from_user.id, msg.message_id)

@dp.message_handler()
async def enter_start(msg: Message):

    status = sql_commands.check_status(msg.chat.id)
    
    if status == 'none':
        await bot.delete_message(msg.from_user.id, msg.message_id)

    elif status == 'reg_name':
        if len(msg.text.split(' ')) == 2 and msg.text.replace(' ','f').isalpha():
            print(123)
            sql_commands.change_in_table('bot', 'INSERT OR IGNORE INTO pre_reg (id, name) VALUES (\'%d\', \'%s\')' % (msg.chat.id, msg.text))

@dp.callback_query_handler()
async def callback(call):

    user_id = call.message.chat.id
    status = sql_commands.check_status(user_id)
    edit = lambda text, markup: bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup)

    if call.data == 'priority_start' and status != 'none':
        sql_commands.set_status(user_id, 'none')
        await edit(MESSAGES['start'], markups.markup_start())
    
    elif status != 'none':
        return
    
    elif call.data == 'start':
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
        await edit(MESSAGES['registration_name'], InlineKeyboardMarkup())


if __name__ == '__main__':
    executor.start_polling(dp)