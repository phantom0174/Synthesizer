from discord.ext import commands
from functions import *
#import keep_alive
import sqlite3
import discord
import asyncio
import json
import sys
import os

with open('setting.json', mode='r', encoding='utf8') as jfile:
    db = json.load(jfile)

connection = sqlite3.connect('DataBase.db')
data = connection.cursor()

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='sc!', intents=intents)

global _ToSQCS
global _ToMV
global _Report

def db_setup():
    # data.execute('DROP TABLE account;')

    '''
    data.execute("""CREATE TABLE IF NOT EXISTS account (
          Id INTEGER,
          Name TEXT,
          PWD TEXT,
          Status INTEGER);""")

    data.connection.commit()
    '''


@bot.event
async def on_ready():
    global _ToSQCS
    global _ToMV
    global _Report

    _ToSQCS = discord.utils.get(bot.guilds[1].text_channels, name='sqcs-and-syn')
    _ToMV = discord.utils.get(bot.guilds[1].text_channels, name='syn-and-mv')
    _Report = discord.utils.get(bot.guilds[1].text_channels, name='syn-report')
    print("------>> Bot is online <<------")
    # db_setup()
    await Admin_auto()


# ping
@bot.command()
async def ping(ctx):
    await ctx.send(f'{round(bot.latency * 1000)} (ms)')


# check member
@bot.command()
async def m_c(ctx):
    for member in ctx.guild.members:
        print(member)


async def Admin_auto():
    guild = bot.guilds[0]

    AdminRole = guild.get_role(int(db['Admin']))
    while (1):
        if (now_time_info('hour') >= 21 or now_time_info('hour') <= 6):
            data.execute('SELECT Id, Status FROM account')
            Accs = data.fetchall()

            for acc in Accs:
                user = await guild.fetch_member(acc[0])
                if (acc[1] == 1):
                    await user.add_roles(AdminRole)
                elif (acc[1] == 0):
                    await user.remove_roles(AdminRole)
        await asyncio.sleep(600)
        await _Report.send(f'[Update]Guild logined member admin role. {now_time_info("whole")}')


# ===== group - account =====>>
# account main group
@bot.group()
async def acc(ctx):
    pass


# check account_list
@acc.command()
async def list(ctx):
    if (role_check(ctx.author.roles, '總召') == False):
        await ctx.send('You can\'t use that command!')
        return

    data.execute('SELECT * FROM account')
    Accs = data.fetchall()

    print(Accs)

    account_info = str()
    for acc in Accs:
        account_info += f'{acc[1]}({acc[0]})<{acc[2]}>: {acc[3]}\n'

    print(account_info)

    await _Report.send(f'[Command]Group acc - list used by member {ctx.author.id}. {now_time_info("whole")}')


# account login
@acc.command()
async def login(ctx):
    data.execute(f'SELECT * FROM account WHERE Id={ctx.author.id}')
    info = data.fetchall()

    if (len(info) == 0):
        await ctx.author.send('You havn\'t register yet!')
        return

    if (info[0][3] == 1):
        await ctx.author.send('You\'ve already login!')
        return

    def check(message):
        return message.channel == ctx.author.dm_channel and message.author == ctx.author

    await ctx.author.send('Enter account: ')
    Acc = (await bot.wait_for('message', check=check, timeout=30.0)).content

    await ctx.author.send('Enter password: ')
    Ps = (await bot.wait_for('message', check=check, timeout=30.0)).content

    if (info[0][1] == Acc and info[0][2] == Ps):
        data.execute(f'UPDATE account SET Status=1 WHERE Id={ctx.author.id};')
        await ctx.author.send('Login Success!')
    else:
        await ctx.author.send('Login Failed.')
        return

    data.connection.commit()

    await _Report.send(f'[Command]Group acc - login used by member {ctx.author.id}. {now_time_info("whole")}')


# account logout
@acc.command()
async def logout(ctx):
    data.execute(f'SELECT * FROM account WHERE Id={ctx.author.id}')
    info = data.fetchall()

    if (len(info) == 0):
        await ctx.author.send('You havn\'t register yet!')
        return

    if (info[0][3] == 0):
        await ctx.author.send('You\'ve already logout!')
        return

    data.execute(f'UPDATE account SET Status=0 WHERE Id={ctx.author.id};')
    await ctx.author.send('Logout Success!')

    data.connection.commit()

    await _Report.send(f'[Command]Group acc - logout used by member {ctx.author.id}. {now_time_info("whole")}')


# register account
@acc.command()
async def register(ctx):
    data.execute(f'SELECT * FROM account WHERE Id={ctx.author.id}')
    info = data.fetchall()

    if (len(info) != 0):
        await ctx.author.send('You\'ve already registered!')
        return

    def check(message):
        return message.channel == ctx.author.dm_channel and message.author == ctx.author

    await ctx.author.send('Set account: ')
    RegName = (await bot.wait_for('message', check=check, timeout=30.0)).content

    await ctx.author.send('Set password: ')
    RegPs = (await bot.wait_for('message', check=check, timeout=30.0)).content

    await ctx.author.send('Password confirming: ')
    PsCfm = (await bot.wait_for('message', check=check, timeout=30.0)).content

    if (RegPs != PsCfm):
        await ctx.author.send('Two password are not the same, please try again registration.')
        return

    # data.execute(f'INSERT INTO account VALUES({ctx.author.id}, {RegName}, {RegPs}, 0);')
    data.execute(f'INSERT INTO account (id, Name, PWD, Status) VALUES ("{ctx.author.id}", "{RegName}", "{RegPs}", 0);')

    await ctx.author.send('Register Success!')

    data.connection.commit()

    await _Report.send(f'[Command]Group acc - register used by member {ctx.author.id}. {now_time_info("whole")}')


# account manipulation
@acc.command()
async def mani(ctx):
    data.execute(f'SELECT * FROM account WHERE Id="{ctx.author.id}"')
    info = data.fetchall()

    print(info)

    if (len(info) == 0):
        await ctx.author.send('You havn\'t register yet!')
        return

    MAcc = str()
    MPs = str()

    def check(message):
        return message.channel == ctx.author.dm_channel and message.author == ctx.author

    await ctx.author.send('Do you want to change account?(yes/no): ')
    AccChg = (await bot.wait_for('message', check=check, timeout=30.0)).content.lower()
    if (AccChg == 'yes'):
        await ctx.author.send('Re-set account: ')
        MAcc = (await bot.wait_for('message', check=check, timeout=30.0)).content
    elif (AccChg != 'no'):
        await ctx.author.send('Invalid syntax!')
        return

    await ctx.author.send('Do you want to change password?(yes/no): ')
    PsChg = (await bot.wait_for('message', check=check, timeout=30.0)).content.lower()
    if (PsChg == 'yes'):
        await ctx.author.send('Re-set password: ')
        MPs = (await bot.wait_for('message', check=check, timeout=30.0)).content

        await ctx.author.send('Password confirming: ')
        PsCfm = (await bot.wait_for('message', check=check, timeout=30.0)).content

        if (MPs != PsCfm):
            await ctx.author.send('Two password are not the same, please try again account manipulation.')
            return
    elif (PsChg != 'no'):
        await ctx.author.send('Invalid syntax!')
        return

    if (AccChg == 'yes'):
        data.execute(f'UPDATE account SET Name="{MAcc}" WHERE Id={ctx.author.id};')
    if (PsChg == 'yes'):
        data.execute(f'UPDATE account SET PWD="{MPs}" WHERE Id={ctx.author.id};')

    await ctx.author.send('Account manipulation success!')

    data.connection.commit()

    await _Report.send(f'[Command]Group acc - mani used by member {ctx.author.id}. {now_time_info("whole")}')


# ===== group - account =====<<


# department role update
@bot.command()
async def role_update(ctx, *, msg):
    if (round(bot.latency * 1000) <= 100):
        await ctx.send('The bot is now hosting on repl.it, please host it on pc to use this command!')
        return

        # Mode:: 1:副召, 2:美宣, 3:網管, 4:公關, 5:議程, 6:管理
    print(msg.split(' '))
    if (len(msg.split(' ')) != 2):
        await ctx.send('There are no target selected!')
        return

    mode = int(msg.split(' ')[0])
    print(mode)

    msg_split = msg.split(' ')[1].split('\n')
    print(msg_split)

    if (int(len(msg_split)) % 2 != 0):
        await ctx.send('School -> Name map error!')
        return

    school = []
    name = []

    new_role = ctx.guild.get_role(int(db['department_id'][mode]))
    await ctx.send(new_role)

    for i in range(int(len(msg_split))):
        if (i + 1 <= int(len(msg_split) / 2)):
            school.append(msg_split[i])
        else:
            name.append(msg_split[i])

    for i in range(int(len(msg_split) / 2)):
        for member in ctx.guild.members:
            member_tag = member.name.split(' ')
            print(member_tag)

            if (len(member_tag) >= 3):
                member_school = member_tag[0]
                member_name = member_tag[1]
                if (member_school.find(school[i]) != -1 and member_name == name[i]):
                    old_role = member.top_role
                    if (len(member.roles) == 2):
                        await member.remove_roles(old_role)
                    await member.add_roles(new_role)
                    await ctx.channel.send(f'{member.name}\'s role was updated to {new_role}!')

    await ctx.send('Role update complete!')

    await _Report.send(f'[Command]role_update used by member {ctx.author.id}. {now_time_info("whole")}')


@bot.command()
async def safe_stop(ctx):
    if (role_check(ctx.author.roles, '總召') == False):
        await ctx.send('You can\'t use that command!')
        return

    print('The bot has stopped!')
    data.connection.commit()
    data.connection.close()
    sys.exit(0)


@bot.event
async def on_disconnect():
    print('Bot disconnected')
    data.connection.commit()


#keep_alive.keep_alive()

bot.run(os.environ.get("TOKEN"))