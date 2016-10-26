import telebot
from conf import token

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['гороскоп', 'horoscope', 'horrorscope'])
def send_horoscope(message):
    reply = 'ваш гороскоп на сегодня представляет {0}: {1}'
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
