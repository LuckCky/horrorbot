# -*- coding: utf-8 -*-
# A simple wrapper on Python 3 Shelve module
# https://docs.python.org/3.5/library/shelve.html

import shelve
from datetime import timedelta, datetime

import conf

def delete_old_prediction(date):
    db = shelve.open(conf.storage_name)
    for delta in range(1, 8):
        try:
            date = date - timedelta(delta)
            del db[date]
        except:
            pass
    db.close()

def set_user_sign(user_id, sign):
    db = shelve.open(conf.storage_name)
    db[str(user_id)] = sign
    db.close()

def set_today_prediction(date, prediction):
    db = shelve.open(conf.storage_name)
    date = date.strftime('%d/%m/%Y')
    db[date] = prediction
    db.close()

def get_today_prediction(date):
    try:
        db = shelve.open(conf.storage_name)
        date = date.strftime('%d/%m/%Y')
        prediction = db[date]
        db.close()
        return prediction
    except KeyError:
        return None

def get_user_sign(user_id):
    try:
        db = shelve.open(conf.storage_name)
        sign = db[str(user_id)]
        db.close()
        return sign
    except KeyError:
        return None
