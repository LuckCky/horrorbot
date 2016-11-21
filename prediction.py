from datetime import datetime
import random

from signs import signs
from dbhelper import delete_old_prediction, set_today_prediction
from dbhelper import get_today_prediction

def line_conter():
    with open('Murpys_laws.txt', 'r') as source:
        for num, line in enumerate(source):
            pass
    return num + 1

def predictor():
    lines_num = line_conter()
    prediction = {}
    lines_nums = random.sample(range(1, lines_num), 12)
    for i in range(0, 12):
        sign = signs[i][0][0]
        prediction[sign] = lines_nums[i]
    set_today_prediction(datetime.now(), prediction)

def read_prediction(sign):
    delete_old_prediction(datetime.now())
    prediction = get_today_prediction(datetime.now())
    with open('Murpys_laws.txt', 'r') as source:
        for num, line in enumerate(source):
            if num == prediction[sign]:
                n = line.find('.')
                return line[:n], line[n+2:].rstrip()
