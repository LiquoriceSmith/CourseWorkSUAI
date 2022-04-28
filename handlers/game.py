from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from SQLighter import read_sqlite_table
from random import shuffle
from create_bot import dp, bot


class Game(StatesGroup):
    count_answer = 0
    count_questions = 1
    q1 = State()


async def cmd_game(message: types.Message):
    generate_markup()
    await bot.send_photo(chat_id=message.chat.id, photo=raw[1])
    await message.answer("Выберите правильный ответ", reply_markup=markup)
    await Game.q1.set()


async def answer(message: types.Message, state: FSMContext):
    Game.count_questions += 1
    await state.update_data(answer1=message.text)
    data = await state.get_data()
    answer1 = data.get('answer1')
    if answer1 == true_answer:
        Game.count_answer += 1
    generate_markup()
    await bot.send_photo(chat_id=message.chat.id, photo=raw[1])
    await message.answer("Выберите правильный ответ", reply_markup=markup)
    if Game.count_questions < 5:
        await Game.q1.set()
    else:
        await state.finish()
        print(Game.count_answer)


def register_handlers_game(dp: Dispatcher):
    dp.register_message_handler(cmd_game, commands=['game'])
    dp.register_message_handler(answer, state=Game.q1)


def generate_markup():
    global markup, raw, true_answer
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    raw = read_sqlite_table()
    print(raw)
    all_answers = raw[2] + ', ' + raw[3]
    all_answers = all_answers.split(', ')
    true_answer = raw[2]
    shuffle(all_answers)
    for item in all_answers:
        markup.add(item)
    return markup
