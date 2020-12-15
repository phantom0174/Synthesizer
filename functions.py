from datetime import datetime, timezone, timedelta
import discord
global _ToSQCS
global _ToMV
global _Report


def now_time_info(mode):
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8)))  # 轉換時區 -> 東八區

    if mode == 'whole':
        return str(dt2.strftime("%Y-%m-%d %H:%M:%S"))
    elif mode == 'hour':
        return int(dt2.strftime("%H"))
    elif mode == 'date':
        return int(dt2.isoweekday())


def list_check(main_list, target_list):
    for main in main_list:
        if (main in target_list):
            return True

    return False


def role_check(main_list, target_list):
    for main in main_list:
        if (main.name in target_list):
            return True

    return False


def cadre_trans(cadre):
    if cadre == '副召':
        return 1
    elif cadre == 1:
        return '副召'

    if cadre == '網管':
        return 2
    elif cadre == 2:
        return '網管'

    if cadre == '議程':
        return 3
    elif cadre == 3:
        return '議程'

    if cadre == '公關':
        return 4
    elif cadre == 4:
        return '公關'

    if cadre == '美宣':
        return 5
    elif cadre == 5:
        return '美宣'

    if cadre == '管理':
        return 6
    elif cadre == 6:
        return '管理'

    if cadre == '一般':
        return 7
    elif cadre == 7:
        return '一般'

    return -1


async def setChannel(bot):
    global _ToSQCS
    global _ToMV
    global _Report

    _ToSQCS = discord.utils.get(bot.guilds[1].text_channels, name='sqcs-and-syn')
    _ToMV = discord.utils.get(bot.guilds[1].text_channels, name='syn-and-mv')
    _Report = discord.utils.get(bot.guilds[1].text_channels, name='syn-report')


def getChannel(target):
    global _ToSQCS
    global _ToMV
    global _Report

    if target == '_ToSQCS':
        return _ToSQCS
    elif target == '_ToMV':
        return _ToMV
    elif target == '_Report':
        return _Report
