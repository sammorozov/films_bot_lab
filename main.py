from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import Bot, Dispatcher, F
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup)
import parser_for_links
import levenstein
import sqlite3
import os

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
 

#кнопочки
button_1 = KeyboardButton(text='1 - Поиск по тексту')
# button_2 = KeyboardButton(text='2 - Получить ссылки')


keyboard = ReplyKeyboardMarkup(
    keyboard=[[button_1]],
    resize_keyboard=True,
    one_time_keyboard=True
)

@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\n'+ 
                         'Для поиска фильма - кнопка №1\n' + 
                         'Для вызова помощи напиши /help \n' +
                         'Для просмотра истории запросов напиши /history \n' +
                         'Для просмотра статистики напиши /stats \n',
                         reply_markup=keyboard)


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'А вот и помощь!\n'
        '1) Кнопка "1 - Поиск по тексту" или напишите название фильма в чат для актуальной ссылки \n\n'
        '2) /history - посмотреть историю ваших запросов \n\n'
        '3) /stats - получить статистику ваших запросов\n\n'
    )


conn = sqlite3.connect('user_history_and_stats.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_history (
        user_id INTEGER,
        query TEXT,
        date_time DATETIME
    )
''')
conn.commit()
conn.close()


# хендлер на историю
@dp.message(Command(commands=['history']))
async def show_history(message: Message):
    user_id = message.from_user.id 

    conn = sqlite3.connect('user_history_and_stats.db')
    cursor = conn.cursor()
    cursor.execute('SELECT query, date_time FROM user_history WHERE user_id=?', (user_id,))
    history = cursor.fetchall()
    conn.close()

    if history:
        response = "История ваших запросов:\n"
        for query, date_time in history:
            response += f"{date_time}: {query}\n"
    else:
        response = "Вы еще ничего не запрашивали :("

    await message.answer(response)



# хэндлер на статистику
@dp.message(Command(commands=['stats']))
async def show_stats(message: Message):
    user_id = message.from_user.id  

    conn = sqlite3.connect('user_history_and_stats.db')
    cursor = conn.cursor()
    cursor.execute('SELECT query, COUNT(query) ' 
                   'FROM user_history WHERE user_id=? '
                   'GROUP BY query '
                   'ORDER BY COUNT(query) DESC; ', (user_id,))
    stats = cursor.fetchall()
    conn.close()

    if stats:

        cnt = 0
        response = "Ваша статистика запросов:\n"
        for query, count in stats:
            if cnt == 0:
                max_resp = query
            cnt += 1

            response += f"{cnt}) {query}: {count} раз(а)\n"

        response += '\nБольше всего вы интересовались фильмом: ' + str(max_resp)
    else:
        response = "Вы еще ничего не запрашивали :(."

    await message.answer(response)




@dp.message(F.text == '1 - Поиск по тексту')
async def example(message: Message):
    await message.answer(
        text='Введите название фильма '
    )


@dp.message()
async def send_echo(message: Message):
    message_text = str(message.text)

    if message_text not in levenstein.hardcode_words:
        await message.answer(str(levenstein.offer(message_text)))

    else:
        resp, link = await parser_for_links.response(message_text)
        await message.answer(str(resp), parse_mode='html')

        if resp:
            await message.answer_photo(link)

            conn = sqlite3.connect('user_history_and_stats.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO user_history (user_id, query, date_time) VALUES (?, ?, DATETIME("now"))',
                           (message.from_user.id, message_text))
            conn.commit()
            conn.close()

            await message.answer('Приятного просмотра!')
         


if __name__ == '__main__':
    dp.run_polling(bot)

# BOT_TOKEN = '6********2:A**********lL-**********D0BksYK87bU'
    
    
