from datetime import datetime, timezone, timedelta
from math import *
import json

def now_time_info(mode):
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8)))  # 轉換時區 -> 東八區

    if(mode == 'whole'):
        return str(dt2.strftime("%Y-%m-%d %H:%M:%S"))
    elif(mode == 'hour'):
        return int(dt2.strftime("%H"))
    elif(mode == 'date'):
        return int(dt2.isoweekday())

def role_check(roles, t_role):
    for role in roles:
        for mrole in t_role:
            if(role.name == mrole):
                return True

    return False

def cadre_check(t_cadre, list):
    for cadre in list:
        if(cadre == t_cadre):
            return True
    return False

def cadre_index_trans(cadre):
    if(cadre == '副召'):
        return 0
    elif(cadre == 0):
        return '副召'
    elif(cadre == '')