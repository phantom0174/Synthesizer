import discord
from discord.ext import commands
import json
import time
import asyncio
from datetime import datetime,timezone,timedelta
import AES

def now_hour():
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8)))  # 轉換時區 -> 東八區
    return int(dt2.strftime("%H"))

with open('database.json', mode='r', encoding='utf8') as jfile:
    db = json.load(jfile)

bot = commands.Bot(command_prefix='sc!')


@bot.event
async def on_ready():
    print("------>> Bot is online <<------")
    #await re_task()

#ping
@bot.command()
async def ping(ctx):
    await ctx.send(f'{round(bot.latency * 1000)} (ms)')

#check member
@bot.command()
async def m_c(ctx):
    for member in ctx.guild.members:
        print(member)

'''
async def re_task():
    channel = bot.guild.get()
    while(1):
        await asyncio.sleep(600)
        if(now_hour >= 21 and )
'''

'''
#check account_list
@bot.command()
async def account_list(ctx):
    temp_file = open('account_data.json', mode='r', encoding='utf8')
    ad = json.load(temp_file) #account data
    temp_file.close()

    CmderIndex = int(0)
    CmderId = str(ctx.author.id)
    IdCheck = int(0)
    for i in range(ad['id']):
        if(ad['id'][i] == CmderId):
            IdCheck = int(1)
            CmderIndex = i
            break

    if (IdCheck == int(0)):
        await ctx.send('You can\'t use that command!')
        return
'''

#account login
@bot.command()
async def login(ctx):
    temp_file = open('account_data.json', mode='r', encoding='utf8')
    ad = json.load(temp_file)  # account data
    temp_file.close()

    UserIndex = int(0)
    UserExist = int(0)

    for i in range(len(ad['id'])):
        if(ad['id'][i] == str(ctx.author.id)):
            UserExist = int(1)
            UserIndex = int(i)
            break

    if(UserExist == int(0)):
        await ctx.author.send('You havn\'t register yet!')
        return


    Acc = str()
    Ps = str()

    def check(message):
        return message.channel == ctx.author.dm_channel and message.author == ctx.author

    await ctx.author.send('Enter account: ')
    Acc = (await bot.wait_for('message', check=check, timeout=30.0)).content

    await ctx.author.send('Enter password: ')
    Ps = (await bot.wait_for('message', check=check, timeout=30.0)).content

    if(ad['account'][UserIndex] == Acc and ad['password'][UserIndex] == Ps):
        ad['status'][UserIndex] = '1'
        await ctx.author.send('Login Success!')
    else:
        ad['status'][UserIndex] = '0'
        await ctx.author.send('Login Failed.')
        return

    temp_file = open('account_data.json', mode='w', encoding='utf8')
    json.dump(ad, temp_file)
    temp_file.close()

#account logout
@bot.command()
async def logout(ctx):
    temp_file = open('account_data.json', mode='r', encoding='utf8')
    ad = json.load(temp_file)  # account data
    temp_file.close()

    UserIndex = int(0)
    UserExist = int(0)

    for i in range(len(ad['id'])):
        if(ad['id'][i] == str(ctx.author.id)):
            UserExist = int(1)
            UserIndex = int(i)
            break

    if(UserExist == int(0)):
        await ctx.author.send('You havn\'t register yet!')
        return

    if(ad['status'][UserIndex] == '0'):
        await ctx.author.send('You\'ve already logout!')
        return

    ad['status'][UserIndex] = '0'
    await ctx.author.send('Logout Success!')

    temp_file = open('account_data.json', mode='w', encoding='utf8')
    json.dump(ad, temp_file)
    temp_file.close()

#register account
@bot.command()
async def register(ctx):
    temp_file = open('account_data.json', mode='r', encoding='utf8')
    ad = json.load(temp_file)  # account data
    temp_file.close()

    for UserId in ad['id']:
        if(str(ctx.author.id) == UserId):
            await ctx.author.send('You\'ve already registered!')
            return

    RegAcc = str()
    RegPs = str()

    def check(message):
        return message.channel == ctx.author.dm_channel and message.author == ctx.author

    await ctx.author.send('Set account: ')
    RegAcc = (await bot.wait_for('message', check=check, timeout=30.0)).content

    await ctx.author.send('Set password: ')
    RegPs = (await bot.wait_for('message', check=check, timeout=30.0)).content

    await ctx.author.send('Password confirming: ')
    PsCfm = (await bot.wait_for('message', check=check, timeout=30.0)).content

    if(RegPs != PsCfm):
        await ctx.author.send('Two password are not the same, please try again registration.')
        return

    ad['account'].append(RegAcc)
    ad['password'].append(RegPs)
    ad['id'].append(str(ctx.author.id))
    ad['status'].append('0')
    await ctx.author.send('Register Success!')

    temp_file = open('account_data.json', mode='w', encoding='utf8')
    json.dump(ad, temp_file)
    temp_file.close()

#account manipulation
@bot.command()
async def account_m(ctx):
    temp_file = open('account_data.json', mode='r', encoding='utf8')
    ad = json.load(temp_file)  # account data
    temp_file.close()

    UserIndex = int(0)
    UserExist = int(0)

    for i in range(len(ad['id'])):
        if (ad['id'][i] == str(ctx.author.id)):
            UserExist = int(1)
            UserIndex = int(i)
            break

    if (UserExist == int(0)):
        await ctx.author.send('You havn\'t register yet!')
        return

    MAcc = str()
    MPs = str()

    def check(message):
        return message.channel == ctx.author.dm_channel and message.author == ctx.author

    await ctx.author.send('Do you want to change account?(yes/no): ')
    AccChg = (await bot.wait_for('message', check=check, timeout=30.0)).content.lower()
    if(AccChg == 'yes'):
        await ctx.author.send('Re-set account: ')
        MAcc = (await bot.wait_for('message', check=check, timeout=30.0)).content
    elif(AccChg != 'no'):
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

    if(AccChg == 'yes'):
        ad['account'][UserIndex] = MAcc
    if(PsChg == 'yes'):
        ad['password'][UserIndex] = MPs

    await ctx.author.send('Account manipulation success!')

    temp_file = open('account_data.json', mode='w', encoding='utf8')
    json.dump(ad, temp_file)
    temp_file.close()


bot.run(db['TOKEN'])