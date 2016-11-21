import telebot

from conf import token
from dbhelper import get_user_sign
from prediction import read_prediction

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['гороскоп', 'horoscope', 'horrorscope'])
def send_horoscope(message):
    sign = get_user_sign(message.message_id)
    if sign:
        prediction = read_prediction(sign)
        reply = 'сегодня ваш день будет определять {0}'.format(prediction[0]) \
                + 'который гласит: {0}'.format(prediction[1])
    else:
        reply = 'Пожалуйста, напишите дату своего рождения в формате ДД/ММ или ДД.ММ'
    bot.reply_to(message, reply)

@bot.message_handler(regexp='ороскоп')
def send_horoscope(message):
    reply = 'ваш гороскоп на сегодня представляет {0}: {1}'
    bot.reply_to(message, reply)

@bot.message_handler(regexp='oroscope')
def send_horoscope(message):
    reply = 'ваш гороскоп на сегодня представляет {0}: {1}'
    bot.reply_to(message, reply)

@bot.message_handler(regexp='orrorscope')
def send_horoscope(message):
    reply = 'ваш гороскоп на сегодня представляет {0}: {1}'
    bot.reply_to(message, reply)

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.polling()
