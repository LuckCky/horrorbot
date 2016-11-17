from signs import signs
from dbhelper import set_user_sign

def parse_date(user_id, birth_date):
    if '/' in birth_date:
        birth_date = birth_date.split('/')
    elif '.' in birth_date:
        birth_date = birth_date.split('.')
    birth_date_day = int(birth_date[0])
    birth_date_month = int(birth_date[1])
    return birth_date_day, birth_date_month

def check_date(birth_date_day, birth_date_month):
    long_months = [1, 3, 5, 7, 8, 10, 12]
    short_months = [4, 6, 9, 11]
    feb = 2
    if birth_date_month in long_months:
        if birth_date_day > 31:
            return False
    elif birth_date_month in short_months:
        if birth_date_day > 30:
            return False
    elif birth_date_month == feb:
        if birth_date_day > 29:
            return False
    return True

def sign_define(user_id, birth_date):
    if birth_date == ['29', '2']:
        # set_user_sign(user_id, 'Рыбы')
        return 'Рыбы'
    for num, k in enumerate(signs):
        end_month = k[1][1][1]
        end_day = k[1][1][0]
        if birth_date_month == end_month:
            if birth_date_day <= end_day:
                # set_user_sign(user_id, signs[num][0])
                return signs[num][0][0]
            else:
                if birth_date_month == 3:
                    # set_user_sign(user_id, 'Рыбы')
                    return 'Рыбы'
                # set_user_sign(user_id, signs[num+1][0])
                return signs[num+1][0][0]
