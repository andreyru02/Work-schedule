from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import InputFile
import glob
import config
from sql import SQL

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)
db = SQL('bd.db')

keyboard = InlineKeyboardMarkup(row_width=2)
graph = InlineKeyboardButton(text='График', callback_data="graph")
list = InlineKeyboardButton(text='Лист', callback_data="list")
date_file = InlineKeyboardButton(text='Дата обновления графика', callback_data="date_file")
keyboard.add(graph, list, date_file)

adm_keyboard = InlineKeyboardMarkup()
prn_bd = InlineKeyboardButton(text='Отправить базу', callback_data='send_bd')
adm_keyboard.add(prn_bd)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    if message.from_user.id == 860916279:
        await bot.send_message(message.from_user.id, 'Выбери действие!', reply_markup=adm_keyboard)
    else:
        await bot.send_message(message.from_user.id, "Выбери действие!", reply_markup=keyboard)
        if not db.subscriber_exists(message.from_user.id):
            # если пользователя нет в базе - добавляем его
            db.add_subscriber(message.from_user.id, message.from_user.first_name, message.from_user.username)


@dp.callback_query_handler()
async def menu(call: types.CallbackQuery):
    if call.data == 'graph':
        if not db.subscriber_exists(call.from_user.id):
            await bot.send_message(call.from_user.id,
                                   'Для продолжения работы требуется перезапуск бота или отправить команду "/start"')
        else:
            await bot.send_message(call.from_user.id, 'Файл загружается.')
            file_graph = InputFile(f'{glob.glob("/home/sa/work_schedule/data/*.xlsm")[0]}')
            await bot.send_document(call.from_user.id, file_graph, reply_markup=keyboard)
            db.add_count_graph(call.from_user.id)
    elif call.data == 'list':
        if not db.subscriber_exists(call.from_user.id):
            await bot.send_message(call.from_user.id,
                                   'Для продолжения работы требуется перезапуск бота или отправить команду "/start"')
        else:
            await bot.send_message(call.from_user.id, 'Функционал еще не реализован.', reply_markup=keyboard)
            db.add_count_list(call.from_user.id)
    elif call.data == 'date_file':
        if not db.subscriber_exists(call.from_user.id):
            await bot.send_message(call.from_user.id,
                                   'Для продолжения работы требуется перезапуск бота или отправить команду "/start"')
        else:
            send_date_file = glob.glob("/home/sa/work_schedule/data/*.xlsm")[0][34:-5]
            await bot.send_message(call.from_user.id, 'Дата изменения графика: ' + send_date_file,
                                   reply_markup=keyboard)
            db.add_count_date_file(call.from_user.id)
    elif call.data == 'send_bd' and call.from_user.id == 860916279:
        await bot.send_message(call.from_user.id, db.read_bd(), parse_mode='Markdown')
    else:
        await bot.send_message(call.from_user.id, 'Неизвестная команда!', reply_markup=keyboard)


if __name__ == '__main__':
    executor.start_polling(dp)
