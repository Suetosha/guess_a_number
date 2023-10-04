import random
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from text import text

ATTEMPTS = 7


class Game:
    def __init__(self):
        self.in_game = False
        self.secret_number = None
        self.attempts = ATTEMPTS
        self.total_games = 0
        self.winning_games = 0
        self.wins = 0

    def generate_random_number(self) -> None:
        self.secret_number = random.randint(1, 100)

    def reset(self) -> None:
        self.total_games += 1
        self.in_game = False
        self.secret_number = None
        self.attempts = ATTEMPTS

    def check_number(self, num) -> str:
        num = int(num)
        if not 0 < num < 101:
            return text['num_range']

        if num == game.secret_number:
            self.winning_games += 1
            self.reset()
            return text['success']

        self.attempts -= 1
        if self.attempts == 0:
            secret_number = game.secret_number
            self.reset()
            return text['zero_attempts'](secret_number)

        if num > self.secret_number:
            return text['lt'](self.attempts)
        else:
            return text['gt'](self.attempts)


TOKEN = 'YOUR TOKEN'
bot = Bot(TOKEN)
dp = Dispatcher()
game = Game()


@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text['welcome'])


@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text['help'](ATTEMPTS))


@dp.message(Command(commands='cancel'))
async def process_cancel_command(message: Message):
    game.reset()
    await message.answer(text['cancel'])
    await message.answer(text['start'])


@dp.message(Command(commands='stat'))
async def process_stat_command(message: Message):
    await message.answer(text['stat'](game.total_games, game.winning_games))


@dp.message(F.text.lower().in_(['да', 'давай', 'сыграем']))
async def process_game_command_yes(message: Message):
    game.generate_random_number()
    game.in_game = True
    await message.answer(text['yes'](game.attempts))


@dp.message(F.text.lower().in_(['нет', 'не хочу', 'в другой раз']))
async def process_game_command_no(message: Message):
    await message.answer(text['cancel'])


@dp.message(lambda x: x.text and x.text.isdigit())
async def process_numbers_answer(message: Message):
    if game.in_game:
        reply_message = game.check_number(message.text)
        await message.answer(reply_message)
    else:
        await message.answer(text['start'])


@dp.message()
async def process_other_answers(message: Message):
    if game.in_game:
        await message.answer(text['not_is_digit'])
    else:
        await message.answer(text['start'])


if __name__ == '__main__':
    dp.run_polling(bot)
