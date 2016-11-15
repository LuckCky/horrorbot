# -*- coding: utf-8 -*-
# A simple wrapper on Python 3 Shelve module
# https://docs.python.org/3.5/library/shelve.html

import shelve
import config


def add_message(message_id, user_id):
    db = shelve.open(config.storage_name)
    db[str(message_id)] = user_id
    db.close()

# Temporally not using this to allow you to answer the same user multiple times
# and/or use ANY message from certain user to write to him
def delete_message(message_id):
    db = shelve.open(config.storage_name)
    del db[str(message_id)]
    db.close()

def get_user_id(message_id):
    try:
        db = shelve.open(config.storage_name)
        uid = db[str(message_id)]
        db.close()
        return uid
    except KeyError:
        return None

def set_user_state(user_id, state_type, state):
    db = shelve.open(config.storage_name)
    db[str(user_id) + state_type] = state
    db.close()

def get_user_state(user_id, state_type):
    try:
        db = shelve.open(config.storage_name)
        state = db[str(user_id) + state_type]
        db.close()
        return state
    except KeyError:
        default_states = {
            'pin': '',
            'actual_pin': (0.0, 0000),
            'auth': False,
            'phone': False,
            'state': None,
            'login': None,
            'keyboard_id': None,
            'pin_keyboard_id': None
        }
        return default_states[state_type]

def get_users():
    db = shelve.open(config.storage_name)
    users = [int(k.strip('start')) for k in db.keys() if 'start' in k]
    db.close()
    return(users)

