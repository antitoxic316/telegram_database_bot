import asyncio
import logging
from aiogram import types, Dispatcher, Router, Bot, exceptions
from aiogram.filters import CommandStart, Command

from database.config import load_config
from database.connect import connect

from func_router import FunctionsRouter
from parser import TextParser
from database.select_queries import Queries


token = "7140653715:AAEYDaNed_rldUKBMZyWULA3V1ktaMgqJY8"

db_connection = connect(load_config("database/database.ini"))

q = Queries(db_connection)
tp = TextParser()
function_r = FunctionsRouter(q, tp)

dp = Dispatcher()

user_router = Router()


@user_router.message(Command("start"))
async def cmd_start(msg: types.Message):
    await msg.answer("hello, you can get a list of available question by /list_questions command")


@user_router.message(Command("list_questions"))
async def cmd_get_data1(msg: types.Message):
    await msg.answer("...")


@user_router.message()
async def process_text(msg: types.Message):
    try:
        select_query_func, func_args = function_r.get_right_function(msg.md_text)
    except ValueError as err:
        await msg.answer(repr(err))
        return

    try:
        if type(func_args) is tuple:
            await msg.answer(select_query_func(*func_args))
        else:
            await msg.answer(select_query_func(func_args))
    except exceptions.TelegramBadRequest as err:
        await msg.answer("Something is wrong with your question")

async def main():
    bot = Bot(token)

    dp.include_router(user_router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())