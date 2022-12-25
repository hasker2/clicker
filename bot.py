import aiogram.utils.exceptions
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.deep_linking import get_start_link, decode_payload
import random
import os
import asyncio
import asyncpg
from aiogram.utils.exceptions import Throttled
from aiogram.contrib.fsm_storage.memory import MemoryStorage

dsn = "dbname='hcnpekzf' user='hcnpekzf' host='mel.db.elephantsql.com' password='cEgK9xYY5la2HnxsLEg6A4c4sTcHYMMV'"
bot = Bot(token="5862467541:AAFnIYv2VCwJICMMhBZwyqRTeYlNP_sn7cA")
allowedlist = ['creator', 'owner', 'admin', 'member']
admins = [5488988760, 1377307544, 5404798380]
checklist = [-1001761893270]
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)





@dp.message_handler(commands=['sendtoall'])
async def process_start_command(message: types.Message):
    conn = await asyncpg.connect(user='owner', password='GjYlPZFaqyEK40VZqh3K5c4mxBQLZvpb',
                                 database='users_fxd8', host='g-a.singapore-postgres.render.com')
    ids = await conn.fetch("select id from users")
    for i in ids:
        await bot.send_message(tuple(i)[0], message.text.split(" ", 1), parse_mode="HTML")

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    conn = await asyncpg.connect(user='owner', password='GjYlPZFaqyEK40VZqh3K5c4mxBQLZvpb',
                                 database='users_fxd8', host='g-a.singapore-postgres.render.com')

    reflink = message.get_args()
    if reflink:
        try:
            mainid = tuple(await conn.fetchrow(f"select id from users where id = {message.chat.id}"))
        except TypeError:
            await conn.execute(f"insert into users (id) values ({message.chat.id})")
            await conn.execute(f"update users set refs = refs + 1 where id = {reflink}")
        except Exception as e:
            print(e)
    a = []
    checkedlist = []
    for i in checklist:
        usersub = await bot.get_chat_member(i, message.from_user.id)
        if usersub.status in allowedlist:
            print(usersub.status)
            checkedlist.append(True)
        else:
            checkedlist.append(False)
        print(checkedlist)

    if False in checkedlist:

        kb = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton(text='Спонсор №1️⃣', url='https://t.me/standoffsila')
        btn3 = types.InlineKeyboardButton(text='✅ПРОВЕРИТЬ✅', callback_data='checksubs')
        kb.row(btn1)
        kb.add(btn3)
        await bot.send_message(message.chat.id, f'Привет {message.from_user.first_name}, этот бот - <b>кликер голды в <u>Standoff 2</u></b>\nНо для начала работы Ты должен подписаться на наших спонсоров по кнопка ниже', parse_mode='HTML', reply_markup=kb)
        await conn.close()
    else:
        kb = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        btn1 = types.KeyboardButton(text='🔥Клик🔥️')
        btn2 = types.KeyboardButton(text='Баланс💵')
        btn3 = types.KeyboardButton(text='Вывод💵⬆')
        btn5 = types.KeyboardButton(text='Отзывы🛒')
        kb.add(btn1)
        kb.row(btn2, btn3)
        kb.row(btn5)
        try:
            await conn.execute(f"insert into users (id) values ({message.chat.id})")
        except Exception as e:
            print(e)

        await bot.send_message(message.chat.id, f'Меню ', reply_markup=kb, parse_mode='HTML')
    await conn.close()
@dp.callback_query_handler(text= ['checksubs'])
async def checksubs(callback: types.CallbackQuery):
    print(callback)
    try:
        first = await bot.get_chat_member(-1001761893270, callback.from_user.id)
        if first.status in allowedlist:
            await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
            kb = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            btn1 = types.KeyboardButton(text='🔥Клик🔥️')
            btn2 = types.KeyboardButton(text='Баланс💵')
            btn3 = types.KeyboardButton(text='Вывод💵⬆')
            btn5 = types.KeyboardButton(text='Отзывы🛒')
            kb.add(btn1)
            kb.row(btn2, btn3)
            kb.row(btn5)
            await bot.send_message(callback.message.chat.id, 'Спасибо за подписку\nТеперь вам доступны все функции бота\n<i>(клавиатура может появиться за пару секунд)</i>', reply_markup=kb, parse_mode='HTML')
        else:
            await bot.answer_callback_query(callback.id, '⚠️Вы не подписались на каналы выше⚠️', show_alert=True)
    except:
        await bot.send_message(callback.message.chat.id, '❗Я не понимаю тебя. Лучше жми /start или используй меню бота (после подписки на спонсоров)')

@dp.message_handler(text='Отзывы🛒')
async def reviews(message: types.Message):
    await bot.send_message(message.chat.id, f'Отзывы \n\nhttps://t.me/clickergolldy_otzivi\nhttps://t.me/clickergolldy_otzivi\nhttps://t.me/clickergolldy_otzivi')

@dp.message_handler(text='🔥Клик🔥️')
@dp.throttled(rate=0.25)
async def click(message: types.Message):
    gold = round(random.uniform(0.1, 1.0), 2)
    await bot.send_message(message.chat.id, f'Вам зачислено <u>{gold}</u> G🔥🔥\nСледующий клик доступен за 0.25 секунды', parse_mode="HTML")
    conn = await asyncpg.connect(user='owner', password='GjYlPZFaqyEK40VZqh3K5c4mxBQLZvpb',
                                 database='users_fxd8', host='g-a.singapore-postgres.render.com')
    await conn.execute(f"update users set balance = balance + {gold} where id = {message.chat.id}")
    await conn.close()

@dp.message_handler(text='Вывод💵⬆')
@dp.throttled(rate=0.5)
async def withdraw(message: types.Message):
    conn = await asyncpg.connect(user='owner', password='GjYlPZFaqyEK40VZqh3K5c4mxBQLZvpb',
                                 database='users_fxd8', host='g-a.singapore-postgres.render.com')
    refs = tuple(await conn.fetchrow(f"select refs from users where id = {message.chat.id}"))[0]
    print(refs)
    gold = tuple(await conn.fetchrow(f"select balance from users where id = {message.chat.id}"))[0]

    link = await get_start_link(str(message.from_user.id))
    if refs < 10:
        await bot.send_message(message.chat.id,
                               f"Для первого вывода вы должни пригласить 10 людей\nВы пригласили {refs}/10\n\nПригласить пользователся можно по вашей ЛИЧНОЙ реферальной ссылке\n{link}\n<i>для того чтобы пользователь засчиталься он должен нажать Start</i>",
                               parse_mode="HTML")
    elif gold < 2155:
        await bot.send_message(message.chat.id,
                               f"‼Вывод начинаеться от 2155 G\n"
                               f"ℹУ вас на балансе {round(gold, 2)}/2155 G\n"
                               f"Такие правила позволяют предотвратить автоматические накрутки🤖",
                               parse_mode="HTML")
    await conn.close()
@dp.message_handler(text='Баланс💵')
@dp.throttled(rate=0.5)
async def click(message: types.Message):
    conn = await asyncpg.connect(user='owner', password='GjYlPZFaqyEK40VZqh3K5c4mxBQLZvpb',
                                 database='users_fxd8', host='g-a.singapore-postgres.render.com')

    balance = tuple(await conn.fetchrow(f"select balance from users where id = {message.chat.id}"))[0]

    await bot.send_message(message.chat.id, f'Ваш баланс = {round(float(balance), 2)} G', parse_mode="HTML")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

    
