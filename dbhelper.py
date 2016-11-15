# -*- coding: utf-8 -*-
# A simple wrapper on Python 3 Shelve module
# https://docs.python.org/3.5/library/shelve.html

import shelve
import conf


def add_message(message_id, user_id):
    db = shelve.open(conf.storage_name)
    db[str(message_id)] = user_id
    db.close()

# Temporally not using this to allow you to answer the same user multiple times
# and/or use ANY message from certain user to write to him
def delete_message(message_id):
    db = shelve.open(conf.storage_name)
    del db[str(message_id)]
    db.close()

def get_user_id(message_id):
    try:
        db = shelve.open(conf.storage_name)
        uid = db[str(message_id)]
        db.close()
        return uid
    except KeyError:
        return None

def set_user_sign(user_id, sign):
    db = shelve.open(conf.storage_name)
    db[str(user_id)] = sign
    db.close()

def get_user_sign(user_id):
    try:
        db = shelve.open(conf.storage_name)
        sign = db[str(user_id)]
        db.close()
        return sign
    except KeyError:
        return None
