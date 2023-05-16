from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from random import randint
from os import environ

bot = Bot(token=environ["BOT_TOKEN"])
dp = Dispatcher(bot, storage=MemoryStorage())


class GameStates(StatesGroup):
    game_beginning = State()
    game_process = State()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.add("Начать")
    await message.reply("Добро пожаловать в игру \"Угадай число\"! " +
                        "Бот загадает число от 1 до 128. Если вы введёте " +
                        "число, бот ответит, больше ли оно загаданного или " +
                        "меньше.\n" +
                        "Чтобы начать, нажмите кнопку.",
                        reply_markup=keyboard)
    await state.set_state(GameStates.game_beginning.state)


@dp.message_handler(Text(equals="Начать"), state=GameStates.game_beginning)
async def cmd_begin(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardRemove()
    await message.reply("Число находится между 1 и 128", reply_markup=keyboard)
    await state.set_state(GameStates.game_process.state)
    await state.update_data(random_value=randint(1, 128))


@dp.message_handler(state=GameStates.game_process)
async def cmd_process(message: types.Message, state: FSMContext):
    data = await state.get_data()
    correct_number = data["random_value"]
    try:
        number = int(message.text)
        if number == correct_number:
            await message.answer("Вы угадали!")
            await state.finish()
        elif number > correct_number:
            await message.answer("Меньше")
        elif number < correct_number:
            await message.answer("Больше")
    except ValueError:
        await message.answer("Вы ввели не число")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
