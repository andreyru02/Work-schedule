from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import InputFile

bot = Bot(token="TOKEN")
dp = Dispatcher(bot)

keyboard = InlineKeyboardMarkup()
graph = InlineKeyboardButton(text='График', callback_data="graph")
list = InlineKeyboardButton(text='Лист', callback_data="list")
keyboard.add(graph, list)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.from_user.id, "Выбери действие!", reply_markup=keyboard)


@dp.callback_query_handler()
async def menu(call: types.CallbackQuery):
    if call.data == 'graph':
        await bot.send_message(call.from_user.id, 'Файл загружается.')
        file_graph = InputFile('/home/sa/work_schedule/data/Grafik.xlsm')
        await bot.send_document(call.from_user.id, file_graph, reply_markup=keyboard)
    elif call.data == 'list':
        await bot.send_message(call.from_user.id, 'Функционал еще не реализован.', reply_markup=keyboard)
    else:
        await bot.send_message(call.from_user.id, 'Неизвестная команда!', reply_markup=keyboard)


if __name__ == '__main__':
    executor.start_polling(dp)