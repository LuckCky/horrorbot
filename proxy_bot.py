#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import telebot
from telebot import types

import config
import dbhelper
from dbhelper import set_user_state, get_user_state, get_users

from collections import defaultdict
import re
import requests

from names import buttons_names, messages, urls, commands

###########################  STATES   ################################

user_state = defaultdict(lambda: None)
user_pin = defaultdict(lambda: "") # pins entered by user
user_actual_pin = defaultdict(lambda: (0.0, 0000)) # actual pins
user_auth = defaultdict(lambda: False)
user_phone = defaultdict(lambda: False)

######################## KEYBOARDS ###################################

def main_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    buttons = []
    for button in ['near', 'balance', 'telephone', 'change', 'card', 'products']:
        buttons.append(types.KeyboardButton(buttons_names[button]))
    markup.row(*buttons[:2])
    markup.row(*buttons[2:4])
    markup.row(*buttons[4:])
    return(markup)

def pin_keyboard(user):
    greeting_text = buttons_names['pin']
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('1', callback_data='1')
    itembtn2 = types.InlineKeyboardButton('2', callback_data='2')
    itembtn3 = types.InlineKeyboardButton('3', callback_data='3')
    itembtn4 = types.InlineKeyboardButton('4', callback_data='4')
    itembtn5 = types.InlineKeyboardButton('5', callback_data='5')
    itembtn6 = types.InlineKeyboardButton('6', callback_data='6')
    itembtn7 = types.InlineKeyboardButton('7', callback_data='7')
    itembtn8 = types.InlineKeyboardButton('8', callback_data='8')
    itembtn9 = types.InlineKeyboardButton('9', callback_data='9')
    itembtn10 = types.InlineKeyboardButton('0', callback_data='0')
    itembtn11 = types.InlineKeyboardButton('Del', callback_data='Del')
    markup.row(itembtn1, itembtn2, itembtn3)
    markup.row(itembtn4, itembtn5, itembtn6)
    markup.row(itembtn7, itembtn8, itembtn9)
    markup.row(itembtn10, itembtn11)
    return(greeting_text, markup)

def auth_keyboard(user_id):
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton(text=buttons_names['auth'], url=urls['auth'] + str(user_id))
    markup.row(itembtn1)
    return(messages['auth'], markup)

def card_keyboard():
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton(text=messages['card'], url=urls['card'])
    markup.row(itembtn1)
    return(messages['card'], markup)

def ucard_keyboard():
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton(text=messages['ucards'], url=urls['ucards'])
    markup.row(itembtn1)
    return(messages['ucards'], markup)

def near_keyboard():
    text = messages['near']
    markup = types.ReplyKeyboardMarkup()
    buttons = []
    for button in ['atms', 'offices', 'main']:
        buttons.append(types.KeyboardButton(buttons_names[button]))
    markup.row(*buttons[:2])
    markup.row(buttons[2])
    return(text, markup)

def location_keyboard():
    text = messages['location']
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton(buttons_names['location'], request_location=True)
    itembtn2 = types.KeyboardButton(buttons_names['cancel'])
    markup.row(itembtn1, itembtn2)
    return(text, markup)

def phone_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('My phone', request_contact=True)
    itembtn2 = types.KeyboardButton(buttons_names['cancel'])
    markup.row(itembtn1, itembtn2)
    return(markup)

def product_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    buttons = []
    for button in ['spend', 'save', 'get_card', 'main']:
        buttons.append(types.KeyboardButton(buttons_names[button]))
    markup.row(*buttons[:2])
    markup.row(*buttons[2:4])
    return(messages['products'], markup)

def spend_keyboard():
    markup = types.InlineKeyboardMarkup()
    buttons = []
    for button in ['credit', 'buyer_credit', 'autocredit', 'home_loan']:
        buttons.append(types.InlineKeyboardButton(buttons_names[button], url=urls[button]))
    buttons.append(types.InlineKeyboardButton(buttons_names['main'], callback_data='main'))
    markup.row(*buttons[:2])
    markup.row(*buttons[2:4])
    markup.row(buttons[4])
    return(messages['spend'], markup)

def save_keyboard():
    markup = types.InlineKeyboardMarkup()
    buttons = []
    for button in ['deposit', 'click', 'investment', 'metals']:
        buttons.append(types.InlineKeyboardButton(buttons_names[button], url=urls[button]))
    buttons.append(types.InlineKeyboardButton(buttons_names['main'], callback_data='main'))
    markup.row(*buttons[:2])
    markup.row(*buttons[2:4])
    markup.row(buttons[4])
    return(messages['save'], markup)

############################ BOT #####################################

bot = telebot.TeleBot(config.token)

######################## HELPER FUNCTIONS ############################

from math import sin, cos, sqrt, atan2, radians
from copy import deepcopy

R = 6373.0

# https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude-python/19412565#19412565
def find_distance(lat1, lon1, lat2, lon2):
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

def find_nearest(object_type, lat, lon):
    if object_type not in storage: 
        return('Dont know what to search', (None, None))
    objects = deepcopy(storage[object_type])
    if not objects: 
        return('Failed to find something near to you.', (None, None))

    distances = {find_distance(lat, lon, *key): key for key in objects}
    nearest = min(list(distances.keys()))
    return(objects[distances[nearest]], distances[nearest])

def get_currencies():
    return(storage['currencies'])

def get_balance(user_id):
    login = get_user_state(user_id, 'login')
    others = """Card: 5189-****-****-2222
Amount: 28,28 EUR 

Card: 5341-****-****-1111
Amount:  28,28 RUR"""
    return {
            'matveev': """Card: 5189-****-****-2828
Amount: 4 500,34 EUR 

Card: 5341-****-****-5693
Amount: 412 431,67 RUR""",

"client": """Card: 5512-****-****-3676
Amount: 530,51 RUR 

Card: 4113-****-****-5693
Amount: 3 432,70 EUR""",

'unicredit':"""Card: 4123-****-****-7831
Amount: 10 931,51 USD 

Card: 4113-****-****-5693
Amount: 2 487,65 RUR"""
}.get(login, others)

def check_pin(user_id):
    pin_creation_time, actual_pin = get_user_state(user_id, 'actual_pin')
    pin = get_user_state(user_id, 'pin')
    pin = int(pin) if pin.isdigit() else 1
    delta = (time.time() - pin_creation_time)/60
    if_active, if_right, message = True, True, ''
    if delta > 1470:
        if_active = False
        messages = 'Pin has expired. Create new pin.'
    elif actual_pin != pin:
        if_right = False
        message = 'Wrong pin. Try again.'
    return(if_active, if_right, message)

def check_pin_keyboard_id(user_id):
    pin_keyboard_id = get_user_state(user_id, 'pin_keyboard_id')
    if pin_keyboard_id:
        try:
            bot.edit_message_text(chat_id = user_id, message_id = pin_keyboard_id, text = buttons_names['pin'] + '.')
        except:
            pass
        set_user_state(user_id, 'pin_keyboard_id', None)

################## COMMANDS AND MESSAGE HANDLERS #####################

@bot.message_handler(commands=["start"])
def command_start(message):
    check_pin_keyboard_id(message.chat.id)
    bot.send_message(message.chat.id, messages['start'], 
                     reply_markup=main_keyboard())
    set_user_state(message.chat.id, 'start', 'start')


@bot.message_handler(commands=["logout"])
def command_logout(message):
    check_pin_keyboard_id(message.chat.id)
    try:
        set_user_state(message.chat.id, 'actual_pin', (0.0, 0))
        requests.get(urls['logout'] + str(message.chat.id))
    except Exception as e:
        print(str(e))

    bot.send_message(message.chat.id, 'Logout', 
                     reply_markup=main_keyboard())


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    symbol = call.data
    user = call.message.chat.id
    if symbol.isdigit():
        current_pin = get_user_state(user, 'pin')
        if len(current_pin) == 3:
            current_pin += symbol
            set_user_state(user, 'pin', current_pin)
            active, right, text = check_pin(call.message.chat.id)
            set_user_state(user, 'pin', '')
            if not active:
                text = 'Pin has expired. Create another pin.'
                _, keyboard = auth_keyboard(call.message.chat.id)
                bot.edit_message_text(chat_id=call.message.chat.id, 
                                      message_id=call.message.message_id, 
                                      text= text, 
                                      reply_markup=keyboard)
            elif not right:
                text = 'Bad pin. Try again.'
                _, keyboard = pin_keyboard(call.message.chat.id)
                bot.edit_message_text(chat_id=call.message.chat.id, 
                                      message_id=call.message.message_id, 
                                      text= text, 
                                      reply_markup=keyboard)
            else:
                state = get_user_state(user, 'state')
                if state == 'balance':
                    text  = get_balance(call.message.chat.id)
                    keyboard = main_keyboard()
                elif state == 'phone':
                    text = "You payment accepted for processing. Thank you!"
                    keyboard = phone_keyboard()
                bot.edit_message_text(chat_id=call.message.chat.id, 
                                      message_id=call.message.message_id, 
                                      text= 'Good pin.')
                bot.send_message(call.message.chat.id, 
                                 text,
                                 reply_markup = main_keyboard())
                set_user_state(call.message.chat.id, 'pin_keyboard_id', None)
        elif len(current_pin) < 4:
            current_pin += symbol
            set_user_state(user, 'pin', current_pin)
            _, markup = pin_keyboard(user)
            bot.edit_message_text(chat_id=call.message.chat.id, 
                                  message_id=call.message.message_id, 
                                  text= 'You entered ' + '*' * len(current_pin), 
                                  reply_markup=markup)
    elif symbol == 'Del':
        current_pin = get_user_state(user, 'pin')
        if len(current_pin) > 0:
            current_pin  = current_pin[:-1]
            set_user_state(user, 'pin', current_pin)
            _, markup = pin_keyboard(user)
            text = 'You entered ' + '*' * len(current_pin)
            bot.edit_message_text(chat_id=call.message.chat.id, 
                                  message_id=call.message.message_id, 
                                  text=text, reply_markup=markup)
    elif symbol == 'main':
        bot.send_message(call.message.chat.id, messages['main'], 
                         reply_markup=main_keyboard())

@bot.message_handler(func=lambda message: True, content_types=["location"])
def my_location(message):
    check_pin_keyboard_id(message.chat.id)
    latitude=message.location.latitude
    longitude=message.location.longitude
    object_type = get_user_state(message.chat.id, 'state')
    nearest, coords = find_nearest(object_type, latitude, longitude)
    bot.send_message(message.chat.id, nearest)
    if all(coords):
        bot.send_location(message.chat.id, 
                          latitude=coords[0], 
                          longitude=coords[1],
                          reply_markup=main_keyboard())

@bot.message_handler(func=lambda message: True, content_types=["contact"])
def my_contact(message):
    check_pin_keyboard_id(message.chat.id)
    if get_user_state(message.chat.id, 'state') == 'phone':
        set_user_state(message.chat.id, 'phone', message.contact.phone_number)
        bot.send_message(message.chat.id, messages['sum'])
    else:
        bot.forward_message(config.my_id, message.chat.id, message.message_id)
        dbhelper.add_message(message.message_id + 1, message.chat.id)
        print(">>>>saving id ={}".format(message.message_id + 1))


@bot.message_handler(func=lambda message: True, content_types=["text"])
def my_text(message):
    check_pin_keyboard_id(message.chat.id)
    sum_re = '[0-9]+'
    phone_re = '[0-9]{11}'
    if re.findall(phone_re, message.text) and get_user_state(message.chat.id, 'state') == 'phone':
        set_user_state(message.chat.id, 'phone', message.text)
        bot.send_message(message.chat.id, messages['sum'])
        return
    elif re.findall(sum_re, message.text) and get_user_state(message.chat.id,'phone'):
        active, right, text = check_pin(message.chat.id)
        set_user_state(message.chat.id, 'pin', '')
        if not active:
            text, keyboard = auth_keyboard(message.chat.id)
            message = bot.send_message(message.chat.id, text, reply_markup=keyboard)
            set_user_state(message.chat.id, 'keyboard_id', message.message_id)
        else:
            text, keyboard = pin_keyboard(message.chat.id)
            pin_keyboard_id = bot.send_message(message.chat.id, text, reply_markup=keyboard)
            set_user_state(message.chat.id, 'pin_keyboard_id', pin_keyboard_id)
        set_user_state(message.chat.id, 'phone', False)
        return
    for regexp in commands:
        if re.findall(regexp, message.text):
            handle_command(commands[regexp], message)
            return


    if message.reply_to_message:
        who_to_send_id = dbhelper.get_user_id(message.reply_to_message.message_id)
        print(">>>>message id from operator={}".format(message.reply_to_message.message_id))
        if who_to_send_id:
            # You can add parse_mode="Markdown" or parse_mode="HTML", however, in this case you MUST make sure,
            # that your markup if well-formed as described here: https://core.telegram.org/bots/api#formatting-options
            # Otherwise, your message won't be sent.
            bot.send_message(who_to_send_id, message.text)
            # Temporarly disabled freeing message ids. They don't waste too much space
            # dbhelper.delete_message(message.reply_to_message.message_id)
    else:
        bot.forward_message(config.my_id, message.chat.id, message.message_id)
        dbhelper.add_message(message.message_id + 1, message.chat.id)
        print(">>>>here saving id ={}".format(message.message_id + 1))
        # bot.send_message(message.chat.id, "Noo one to reply! ")

def handle_command(command, message):
    if command == 'near':
        text, keyboard = near_keyboard()
        bot.send_message(message.chat.id, text, reply_markup=keyboard)
    elif command in ['atms', 'offices']:
        set_user_state(message.chat.id, 'state', command)
        text, keyboard = location_keyboard()
        bot.send_message(message.chat.id, text, reply_markup=keyboard)
    elif command in ['cancel', 'main']:
        bot.send_message(message.chat.id, messages['main'], reply_markup=main_keyboard())
    elif command  == 'change':
        bot.send_message(message.chat.id, get_currencies())
    elif command == 'card':
        text, keyboard = card_keyboard()
        bot.send_message(message.chat.id, text, reply_markup=keyboard)
    elif command == 'ucards':
        text, keyboard = ucard_keyboard()
        bot.send_message(message.chat.id, text, reply_markup=keyboard)
    elif command == 'products':
        text, keyboard = product_keyboard()
        bot.send_message(message.chat.id, text, reply_markup=keyboard)
    elif command == 'save':
        text, keyboard = save_keyboard()
        bot.send_message(message.chat.id, text, reply_markup=keyboard)
    elif command == 'spend':
        text, keyboard = spend_keyboard()
        bot.send_message(message.chat.id, text, reply_markup=keyboard)
    elif command  == 'balance':
        active, right, text = check_pin(message.chat.id)
        set_user_state(message.chat.id, 'pin', '')
        set_user_state(message.chat.id, 'state', 'balance')
        if not active:
            text, keyboard = auth_keyboard(message.chat.id)
            message = bot.send_message(message.chat.id, text, reply_markup=keyboard)
            set_user_state(message.chat.id, 'keyboard_id', message.message_id)
        else:
            text, keyboard = pin_keyboard(message.chat.id)
            pin_keyboard_id = bot.send_message(message.chat.id, text, reply_markup=keyboard)
            set_user_state(message.chat.id, 'pin_keyboard_id', pin_keyboard_id.message_id)
    elif command == 'phone':
        set_user_state(message.chat.id, 'state', 'phone')
        bot.send_message(message.chat.id, messages['phone'], reply_markup=phone_keyboard())



########################## OLD STUFF ####################################

@bot.message_handler(func=lambda message: message.chat.id == config.my_id, content_types=["sticker"])
def my_sticker(message):
    print(">>>>sticker message")
    if message.reply_to_message:
        who_to_send_id = dbhelper.get_user_id(message.reply_to_message.message_id)
        if who_to_send_id:
            bot.send_sticker(who_to_send_id, message.sticker.file_id)
    else:
        bot.send_message(message.chat.id, "No one to reply!")

@bot.message_handler(func=lambda message: message.chat.id == config.my_id, content_types=["photo"])
def my_photo(message):
    print(">>>>photo message")
    if message.reply_to_message:
        who_to_send_id = dbhelper.get_user_id(message.reply_to_message.message_id)
        if who_to_send_id:
            # Send the largest available (last item in photos array)
            bot.send_photo(who_to_send_id, list(message.photo)[-1].file_id)
    else:
        bot.send_message(message.chat.id, "No one to reply!")

@bot.message_handler(func=lambda message: message.chat.id == config.my_id, content_types=["voice"])
def my_voice(message):
    print(">>>>sticker voice")
    if message.reply_to_message:
        who_to_send_id = dbhelper.get_user_id(message.reply_to_message.message_id)
        if who_to_send_id:
            # bot.send_chat_action(who_to_send_id, "record_audio")
            bot.send_voice(who_to_send_id, message.voice.file_id, duration=message.voice.duration)
    else:
        bot.send_message(message.chat.id, "No one to reply!")

@bot.message_handler(func=lambda message: message.chat.id == config.my_id, content_types=["document"])
def my_document(message):
    print(">>>>sticker document")
    if message.reply_to_message:
        who_to_send_id = dbhelper.get_user_id(message.reply_to_message.message_id)
        if who_to_send_id:
            # bot.send_chat_action(who_to_send_id, "upload_document")
            bot.send_document(who_to_send_id, data=message.document.file_id)
    else:
        bot.send_message(message.chat.id, "No one to reply!")

@bot.message_handler(func=lambda message: message.chat.id == config.my_id, content_types=["audio"])
def my_audio(message):
    print(">>>>sticker audio")
    if message.reply_to_message:
        who_to_send_id = dbhelper.get_user_id(message.reply_to_message.message_id)
        if who_to_send_id:
            # bot.send_chat_action(who_to_send_id, "upload_audio")
            bot.send_audio(who_to_send_id, performer=message.audio.performer,
                           audio=message.audio.file_id, title=message.audio.title,
                           duration=message.audio.duration)
    else:
        bot.send_message(message.chat.id, "No one to reply!")

@bot.message_handler(func=lambda message: message.chat.id == config.my_id, content_types=["video"])
def my_video(message):
    print(">>>>sticker video")
    if message.reply_to_message:
        who_to_send_id = dbhelper.get_user_id(message.reply_to_message.message_id)
        if who_to_send_id:
            # bot.send_chat_action(who_to_send_id, "upload_video")
            bot.send_video(who_to_send_id, data=message.video.file_id, duration=message.video.duration)
    else:
        bot.send_message(message.chat.id, "No one to reply!")

###################### MESSAGE FORWARDING ###############################

# Handle all incoming messages except group ones
@bot.message_handler(func=lambda message: message.chat.id != config.my_id,
                     content_types=['text', 'audio', 'document', 'photo', 'sticker', 'video',
                                    'voice', 'location', 'contact'])
def check(message):
    # Forward all messages from other people and save their message_id + 1 to shelve storage.
    # +1, because message_id = X for message FROM user TO bot and
    # message_id = X+1 for message FROM bot TO you

    bot.forward_message(config.my_id, message.chat.id, message.message_id)
    dbhelper.add_message(message.message_id + 1, message.chat.id)
    print(">>>>saving id ={}".format(message.message_id + 1))

######################### TORNADO APP #####################################

import tornado.ioloop
import tornado.web
from threading import Thread
import json
import time

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

    def post(self):
        body = tornado.escape.json_decode(self.request.body)
        pin = int(body['pin'])
        user_id = int(body['user_id'])
        login = body.get('login')

        # save pin
        set_user_state(user_id, 'actual_pin', (time.time(), pin))
        set_user_state(user_id, 'login', login)

        # send pin-keyboard to user
        text, keyboard = pin_keyboard(user_id)
        pin_keyboard_id = bot.send_message(user_id, text, reply_markup=keyboard)
        set_user_state(user_id, 'pin_keyboard_id', pin_keyboard_id.message_id)

        # delete auth button
        keyboard_id = get_user_state(user_id, 'keyboard_id')
        if keyboard_id:
            try:
                bot.edit_message_text(chat_id=user_id, 
                                  message_id=keyboard_id, 
                                  text= messages['auth'])
            except:
                pass


def make_app():
    return tornado.web.Application([(r"/", MainHandler)])

###################### THE WHOLE APP #####################################
import sys

if __name__ == "__main__":
    
    # tornado app to recieve notifications about user login
    app = make_app()
    app.listen(config.port)
    t1 = Thread(target=tornado.ioloop.IOLoop.current().start)
    t1.daemon = True
    t1.start()

    # atms, offices and currencies data updater
    from xml_data_reader import storage, xml_updater
    t2 = Thread(target=xml_updater)
    t2.daemon = True
    t2.start()

    # send updates
    # if 'start' in sys.argv:
    #     users = get_users()
    #     for user in users:
    #         bot.send_message(user, text="Hello, I've got new capabilities!", reply_markup=main_keyboard())

    # send updates
    start = open('start').read().strip()
    if start:
        st = open('start', 'w')
        st.write('')
        st.close()
        users = get_users()
        for user in users:
            bot.send_message(user, text="Hello, I've got new capabilities!", reply_markup=main_keyboard())

    # start polling
    bot.polling(none_stop=True)
