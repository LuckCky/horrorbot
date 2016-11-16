from signs import signs
from dbhelper import set_user_sign

def sign_define(user_id, birth_date):
    if '/' in birth_date:
        birth_date = birth_date.split('/')
    elif '.' in birth_date:
        birth_date = birth_date.split('.')
    if birth_date == ['29', '2']:
        return 'Рыбы'
    birth_date = (int(birth_date[0]), int(birth_date[1]))
    for k in signs:
        start = signs[k][0]
        end = signs[k][1]
        if birth_date <= end:
            # set_user_sign(user_id, k)
            return k

print(sign_define(11, '30.12'))
