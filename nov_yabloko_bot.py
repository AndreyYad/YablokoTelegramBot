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

async def see_table(cmd):
    conn = connect('data/yabloko_tables.sql')
    cur = conn.cursor()

    cur.execute(cmd)
    voters = cur.fetchall()

    info = []

    for el in voters:
        info.append({'name'})
    
    cur.close()
    conn.close()

    return info

@dp.message_handler(commands = ['start'])
async def start_func(msg: Message):

    sql_commands.change_in_table('CREATE TABLE IF NOT EXISTS users (id int primary key, status varchar(50))')
    sql_commands.change_in_table('INSERT OR IGNORE INTO users VALUES (\'%d\', \'none\')' % (msg.chat.id))

    await bot.send_message(msg.from_user.id, MESSAGES['start'], reply_markup=markups.markup_start())

@dp.message_handler()
async def enter_start(msg: Message):

    status = sql_commands.check_status(msg.chat.id)
    
    if status == 'none':
        await bot.delete_message(msg.from_user.id, msg.message_id)

@dp.callback_query_handler()
async def callback(call):

    edit = lambda text, markup: bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

    if call.data == 'start':
        await edit(MESSAGES['start'], markups.markup_start())
    
    elif call.data == 'party_program_select':
        await edit(MESSAGES['party_program_select'], markups.markup_party_program_select())

    elif call.data == 'party_program_federal':
        await edit(MESSAGES['party_program_federal'], markups.markup_party_program_back())

    elif call.data == 'party_program_novgorod':
        await edit(MESSAGES['party_program_novgorod'], markups.markup_party_program_back())


if __name__ == '__main__':
    executor.start_polling(dp)