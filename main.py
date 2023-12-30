from telebot import TeleBot, types
import sqlite3
import threading
from config import BOT_TOKEN
from api_module import min_instId, max_instId, min_price, max_price, prices_in_rub

bot = TeleBot(BOT_TOKEN)

db_lock = threading.Lock()

def get_db_connection():
    return sqlite3.connect('user_history.db')

@bot.message_handler(commands=['hello-world'])
def hello_world(message):
    bot.reply_to(message, "Hello, World!")

@bot.message_handler(func=lambda message: message.text == 'Привет')
def greet(message):
    bot.reply_to(message, "Привет!")

def get_cryptolist():
    crypto_list = []
    for item in prices_in_rub:
        crypto_currency_name = item[1]
        crypto_currency_name = crypto_currency_name.split('-')[0]
        crypto_list.append(crypto_currency_name)
    markup = types.InlineKeyboardMarkup()
    for crypto in crypto_list:
        button = types.InlineKeyboardButton(text=crypto, callback_data=crypto)
        markup.add(button)
    return markup

@bot.message_handler(commands=['low'])
def low(message):
    bot.reply_to(message, f"Самая дешёвая криптовалюта: {min_instId}, цена: {min_price} руб.")
    markup = get_cryptolist()
    bot.send_message(message.chat.id, "Полный список криптовалют:", reply_markup=markup)
    threading.Thread(target=update_user_history, args=(message.chat.id, f"/low {min_instId} - {min_price} руб.")).start()

@bot.message_handler(commands=['high'])
def high(message):
    bot.reply_to(message, f"Самая дорогая криптовалюта: {max_instId}, цена: {round(max_price,2)} руб.")
    markup = get_cryptolist()
    bot.send_message(message.chat.id, "Полный список криптовалют:", reply_markup=markup)
    threading.Thread(target=update_user_history, args=(message.chat.id, f"/high {max_instId} - {round(max_price,2)} руб.")).start()

@bot.message_handler(commands=['custom'])
def custom(message):
    markup = get_cryptolist()
    bot.send_message(message.chat.id, "Полный список криптовалют:", reply_markup=markup)
    threading.Thread(target=update_user_history, args=(message.chat.id, "/custom")).start()

@bot.message_handler(commands=['history'])
def history(message):
    user_id = message.chat.id
    user_history = get_user_history(user_id)
    if user_history:
        bot.send_message(user_id, "История запросов:\n" + "\n".join(user_history))
    else:
        bot.send_message(user_id, "История команд недоступна.")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    for tup in prices_in_rub:
        if call.data in tup[1]:
            price = tup[0]
            break

    bot.answer_callback_query(call.id, f"Цена: {round(price,2)} руб.")
    threading.Thread(target=update_user_history, args=(call.message.chat.id, f"Callback query - {call.data} - {round(price,2)} руб.")).start()

def update_user_history(user_id, command):
    with db_lock:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO user_history VALUES (?, ?)', (user_id, command))
        conn.commit()
        conn.close()

def get_user_history(user_id):
    with db_lock:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT command FROM user_history WHERE user_id=? ORDER BY ROWID DESC LIMIT 10', (user_id,))
        result = [row[0] for row in cursor.fetchall()]
        conn.close()
        return result

bot.polling()
