from datetime import datetime, date

from signs import signs
from dbhelper import set_user_sign

def sign_define(user_id, birth_date):
    birth_date = datetime.strptime(birth_date, '%d.%m')#.strftime('%d.%m')
    for k in signs:
        start = datetime.strptime(signs[k][0], '%d.%m')#.strftime('%d.%m')
        end = datetime.strptime(signs[k][1], '%d.%m')#.strftime('%d.%m')
        if start <= birth_date <= end:
            # set_user_sign(user_id, k)
            return k

print(sign_define(11, '30.12'))
