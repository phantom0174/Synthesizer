from datetime import datetime, timezone, timedelta
from math import *
import json

def now_hour():
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8)))  # 轉換時區 -> 東八區
    return int(dt2.strftime("%H"))

def role_check(roles, t_role):
    Exist = bool(False)
    for role in roles:
        if(role.name == t_role):
            Exist = bool(True)
            break
    return Exist