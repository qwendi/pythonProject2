import asyncio
import random

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart

from config import TOKEN

BOT_TOKEN = TOKEN
bot = Bot(BOT_TOKEN)  # Объект бота
dp = Dispatcher()  # Диспетчер


#данные пользователя
user: dict = {'in_game': False,
              'secret_number': None,
              'wins': 0}


# число от 1 до 100
def get_random_number() -> int:
    return random.randint(1, 100)


# /start
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer('Привет!\nДавай сыграем в игру "Угадай число"?\n\n')


# соглашается поиграть
@dp.message(F.text.lower().in_(['да', 'давай', 'сыграем', 'игра', 'играть', 'хочу играть']))
async def process_positive_answer(message: Message):
    if not user['in_game']:
        user['in_game'] = True
        user['secret_number'] = get_random_number()
        await message.answer('Ура :)\n\nЯ загадал число от 1 до 100, попробуй угадать!')
    else:
        await message.answer('Пока мы играем в игру я могу реагировать только на числа от 1 до 100 ')


# пользователь отказывается
@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def process_negative_answer(message: Message):
    if not user['in_game']:
        await message.answer('Жаль :(\n\nЕсли захочешь поиграть - просто напиши об этом ;)')
    else:
        await message.answer('Мы же сейчас играем. Присылай числа от 1 до 100')


# пользователь вводит числа от 1 до 100
@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    if user['in_game']:
        if int(message.text) == user['secret_number']:
            user['in_game'] = False
            user['wins'] += 1
            await message.answer('Ура!!! Ты угадал число!\n\n'
                                 'Может, сыграем еще?')
        elif int(message.text) > user['secret_number']:
            await message.answer('Мое число меньше ;)')
        elif int(message.text) < user['secret_number']:
            await message.answer('Мое число больше ;)')

    else:
        await message.answer('Мы еще не играем. Хочешь сыграть?')


#любые другие сообщения
@dp.message()
async def process_other_answers(message: Message):
    if user['in_game']:
        await message.answer('Мы же сейчас играем. '
                             'Присылай числа от 1 до 100')
    else:
        await message.answer('Я ничего не знаю кроме игры, давайте просто сыграем!')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
