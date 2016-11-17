from signs import signs
from dbhelper import set_user_sign

def sign_define(user_id, birth_date):
    if '/' in birth_date:
        birth_date = birth_date.split('/')
    elif '.' in birth_date:
        birth_date = birth_date.split('.')
    if birth_date == ['29', '2']:
        return 'Рыбы'
    birth_date_day = int(birth_date[0])
    birth_date_month = int(birth_date[1])
    birth_date = (birth_date_day, birth_date_month)
    for num, k in enumerate(signs):
        start = k[1][0]
        end_month = k[1][1][1]
        end_day = k[1][1][0]
        if birth_date_month == end_month:
            if birth_date_day <= end_day:
                # set_user_sign(user_id, signs[num][0])
                return signs[num][0]
            else:
                # set_user_sign(user_id, signs[num+1][0])
                return signs[num+1][0]
