from aiogram import Bot
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor, exceptions
from aiogram.bot import bot

import asyncio

from modules.config import TOKEN
from modules.messages import MESSAGES
import modules.markups as murkups

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands = ['start'])
async def hello_msg(msg: Message):
    await bot.send_message(msg.from_user.id, MESSAGES['start'], reply_markup=murkups.markup_start())

@dp.callback_query_handler()
async def callback(call):

    edit = lambda text, markup: bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

    if call.data == 'start':
        await edit(MESSAGES['start'], murkups.markup_start())
    
    elif call.data == 'party_program':
        await edit(MESSAGES['party_program_select'], murkups.markup_party_program_select())


if __name__ == '__main__':
    executor.start_polling(dp)