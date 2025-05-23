import keys
import logging
import asyncio
from aiogram import Bot, Dispatcher,  types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder
import requests
import time
import threading
from db import Connect
bot = Bot(token=keys.local.token)

dp = Dispatcher()

DownloadUrl = f'https://api.telegram.org/file/bot{keys.local.token}/'


@dp.message(CommandStart())
async def command_start(message: types.Message):
    markup = ReplyKeyboardMarkup(input_field_placeholder="Выберите из меню",
                                 keyboard=[[KeyboardButton(text="☕Menu")]], resize_keyboard=True)
    text = '''
    <b>👋 Добро пожаловать в кофейню CoffeeScript</b>!
    <blockquote>☕ Здесь рождаются ароматы, пробуждаются вкусы и встречаются те, кто любит кофе не меньше, чем уют.</blockquote>
            Я — ваш персональный бот-бариста. Мои основные функции:
            
            <b>1️⃣ Помощь:</b> Могу помочь сделать заказ
            <b>2️⃣ Бронирование:</b> Оформить бронь столика
            <b>3️⃣ Информирование:</b> Рассказать об акциях и скидках
            <b>4️⃣ Лояльность:</b> Начислять бонусы в программе лояльности.    

    '''
    await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup, parse_mode='HTML')


async def Check(id):
    db = Connect(id=id)
    return await db.GetData()


@dp.message(F.text == '☕Menu')
async def Menu(message: types.Message):
    # print(message)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)    
    markup = InlineKeyboardBuilder([])
    text = '''
    Наше меню:
        ☕ Кофе
        🧋 Холодные напитки
        🍰 Десерты
        🥪 Сэндвичи \/ закуски
        🧩 Сезонные предложения
        🛒 Комбо\-наборы
        🧾 Посмотреть весь чек
        '''
    markup.add(InlineKeyboardButton(text="☕ Кофе", callback_data="Кофе"))
    markup.add(InlineKeyboardButton(
        text="🧋 Холодные напитки", callback_data="Холодные напитки"))
    markup.add(InlineKeyboardButton(text="🍰 Десерты", callback_data="Десерты"))
    markup.add(InlineKeyboardButton(text="🥪 Сэндвичи / закуски",
               callback_data="Сэндвичи / закуски"))
    markup.add(InlineKeyboardButton(text="🧩 Сезонные предложения",
               callback_data="Сезонные предложения"))
    markup.add(InlineKeyboardButton(
        text="🛒 Комбо-наборы", callback_data="Комбо-наборы"))
    markup.add(InlineKeyboardButton(text="🧾 Посмотреть весь чек",
               callback_data="Посмотреть весь чек"))
    await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup.adjust(2).as_markup(), parse_mode='MarkdownV2')


@dp.callback_query()
async def callback(call: types.CallbackQuery):

    if call.data == "Кофе":
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id, request_timeout=5)
        
        text = '''
    ☕ Кофе:
        *Американо – 3 AZN*
        *Капучино – 4 AZN*
        *Латте – 4\.5 AZN*
        *Эспрессо – 2\.5 AZN*
        *Флет уайт – 5 AZN*
        *Раф – 5 AZN*
        '''

        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙Назад", callback_data="Menu"),
             InlineKeyboardButton(text="🧾Посмотреть весь чек", callback_data="Посмотреть весь чек")],

            [InlineKeyboardButton(text="Американо", callback_data="Американо"), InlineKeyboardButton(text="Капучино", callback_data="Капучино"),
             InlineKeyboardButton(text="Латте", callback_data="Латте")],

            [InlineKeyboardButton(text="Эспрессо", callback_data="Эспрессо"),
             InlineKeyboardButton(text="Флет уайт", callback_data="Флет уайт"),
             InlineKeyboardButton(text="Раф", callback_data="Раф")],
        ])
        await bot.send_message(chat_id=call.from_user.id, text=text, reply_markup=markup, parse_mode='MarkdownV2')
    
    
    
    elif call.data == 'Холодные напитки':
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id, request_timeout=5)
        text = '''
    <b>🧋 Холодные напитки:</b>
        • Айс Латте – 9.5 AZN
        • Айс Американо – 3.5 AZN
        • Лимонад (цитрус, ягодный) – 6.5 AZN
        • Милкшейк (шоколад, ваниль) – 1.5 AZN
    '''
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙Назад", callback_data="Menu"),

             InlineKeyboardButton(text="🧾Посмотреть весь чек", callback_data="Посмотреть весь чек")],

            [InlineKeyboardButton(text="Айс Латте", callback_data="Айс Латте"),

             InlineKeyboardButton(text="Айс Американо",
                                  callback_data="Айс Американо")],

            [InlineKeyboardButton(
                text="Лимонад (цитрус, ягодный)", callback_data="Лимонад (цитрус, ягодный)"),

             InlineKeyboardButton(text="Милкшейк (шоколад, ваниль)", callback_data="Милкшейк (шоколад, ваниль)")]
        ])
        await bot.send_message(chat_id=call.from_user.id, text=text, reply_markup=markup, parse_mode='HTML')
    
    
    
    elif call.data == 'Десерты':
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id, request_timeout=5)

        text = '''
        <b>🍰 Десерты:</b>
            • Чизкейк Нью-Йорк – 3 AZN
            • Брауни – 4 AZN
            • Наполеон – 2.6 AZN
            • Круассан (классический / с миндалём) – 4.5 AZN'''
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙Назад", callback_data="Menu"),
             InlineKeyboardButton(text="🧾Посмотреть весь чек", callback_data="Посмотреть весь чек")],
            [InlineKeyboardButton(text="Чизкейк Нью-Йорк", callback_data="Чизкейк Нью-Йорк"),
             InlineKeyboardButton(text="Брауни", callback_data="Брауни"),
             InlineKeyboardButton(text="Наполеон", callback_data="Наполеон")],
            [InlineKeyboardButton(text="Круассан (классический / с миндалём)",
                                  callback_data="Круассан ")],
        ])
        await bot.send_message(chat_id=call.from_user.id, text=text, reply_markup=markup, parse_mode='HTML')



    
    elif call.data == 'Сэндвичи / закуски':
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id, request_timeout=5)

        text = '''
    <b>🥪 Сэндвичи / закуски:</b>
        <b>1. Классический сэндвич с курицей – 3 AZN </b>
            🍗 Куриное филе, сыр чеддер, листья салата, томаты и соус айоли в пшеничном хлебе.

       <b> 2. Панини с моцареллой и томатами – 4 AZN </b>
            🧀 Тёплый сэндвич с расплавленной моцареллой, базиликом и вялеными томатами.

        <b>3. Сэндвич «Цезарь» – 4.5 AZN </b>
            🥬 Ломтики курицы, пармезан, салат айсберг, соус «Цезарь» в чиабатте.

       <b> 4. Хрустящие сырные палочки – 5 AZN </b>
            🧀 Подаются с томатным соусом и свежей зеленью.

        <b>5. Мини-брускетты с паштетом и клюквой – 4.5 AZN </b>
            🍞 Три кусочка багета с домашним паштетом, клюквой и микрозеленью.

        <b>6. Сэндвич с тунцом – 5.7 AZN </b>
            🐟 Тунец, свежий огурец, салат, яйцо и горчичный соус.

        <b>7. Веган-сэндвич с хумусом – 2.5 AZN</b>
            🌱 Хумус, запечённые овощи, шпинат и хлеб из цельного зерна.'''
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔙Назад", callback_data="Menu"),
             InlineKeyboardButton(text="🧾Посмотреть весь чек", callback_data="Посмотреть весь чек")],
            
            [InlineKeyboardButton(text="", callback_data="Классический сэндвич с курицей"),
             InlineKeyboardButton(text="Панини с моцареллой и томатами", callback_data="Панини с моцареллой и томатами")],
            
            [InlineKeyboardButton(text="Сэндвич «Цезарь»", callback_data="Сэндвич «Цезарь»"),
             InlineKeyboardButton(text="Хрустящие сырные палочки", callback_data="Хрустящие сырные палочки")],
            
            [InlineKeyboardButton(text="Мини-брускетты с паштетом и клюквой", callback_data="Мини-брускетты"),
             InlineKeyboardButton(text="Сэндвич с тунцом", callback_data="Сэндвич с тунцом")],
            
            [InlineKeyboardButton(
                text="Веган-сэндвич с хумусом", callback_data="Веган-сэндвич с хумусом")],
        ])
        await bot.send_message(chat_id=call.from_user.id, text=text, reply_markup=markup, parse_mode='HTML')
    
    
    elif call.data == 'Menu':
        # await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id, request_timeout=5)  
        await Menu(call.message)
    

    elif call.data == 'Посмотреть весь чек':
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id, request_timeout=5)
        checkdata=await Check(call.from_user.id)
        text=''
        for i in checkdata:
            text+=f'<b>{i}</b>\n'
        if text:

            await bot.send_message(chat_id=call.from_user.id, text=text, parse_mode='HTML')
        else:
            await bot.send_message(chat_id=call.from_user.id, text='Ваш чек пуст', parse_mode='HTML')
    
    else:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id, request_timeout=5)
        connect=Connect(call.from_user.id)
        response=await Connect(call.from_user.id).Add(chekced=call.data)
        if response:
            await bot.send_message(chat_id=call.from_user.id, text='Товар добавлен в ваш чек', parse_mode='HTML')
        else:
            await bot.send_message(chat_id=call.from_user.id, text='Товар уже есть в вашем чеке', parse_mode='HTML')












async def main():
    await dp.start_polling(bot)
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped")
    except Exception as err:
        logging.error("Error", err)
