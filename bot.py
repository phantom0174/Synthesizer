import discord
from discord.ext import commands
import json
import time
import asyncio
#import keep_alive
from datetime import datetime,timezone,timedelta


def now_hour():
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8)))  # 轉換時區 -> 東八區
    return int(dt2.strftime("%H"))


with open('database.json', mode='r', encoding='utf8') as jfile:
    db = json.load(jfile)

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='sc!', intents=intents)


@bot.event
async def on_ready():
    print("------>> Bot is online <<------")


# ping
@bot.command()
async def ping(ctx):
    await ctx.send(f'{round(bot.latency * 1000)} (ms)')
    await ctx.send('\*~\* Synthesizer hello!')


# check member
@bot.command()
async def m_c(ctx):
    for member in ctx.guild.members:
        print(member)


# auto job activate
@bot.command()
async def re(ctx):
    await ctx.send('Re-progress set!')
    AdminRole = ctx.guild.get_role(int(db['Admin']))
    while (1):
        temp_file = open('account_data.json', mode='r', encoding='utf8')
        ad = json.load(temp_file)  # account data
        temp_file.close()

        if (now_hour() >= 21 or now_hour() <= 6):
            for i in range(len(ad['status'])):
                user = await ctx.guild.fetch_member(int(ad['id'][i]))
                if (ad['status'][i] == '1'):
                    await user.add_roles(AdminRole)
                elif (ad['status'][i] == '0'):
                    await user.remove_roles(AdminRole)

        await asyncio.sleep(600)


#===== group - account =====>>
#account main group
@bot.group()
async def acc(ctx):
    pass

# check account_list
@acc.command()
async def list(ctx):
    role_bool = int(0)
    for role in ctx.author.roles:
        if (str(role) == '總召'):
            role_bool = int(1)
            break

    if (role_bool == int(0)):
        await ctx.send('You can\'t use that command!')
        return

    temp_file = open('account_data.json', mode='r', encoding='utf8')
    ad = json.load(temp_file)  # account data
    temp_file.close()

    account_info = str()
    for i in range(len(ad['account'])):
        account_info += ad['account'][i] + ', ' + ad['id'][i] + ', ' + ad['password'][i] + ', ' + ad['status'][i]
        account_info += '\n'

    print(account_info)

# account login
@acc.command()
async def login(ctx):
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

    if (ad['status'][UserIndex] == '1'):
        await ctx.author.send('You\'ve already login!')
        return

    Acc = str()
    Ps = str()

    def check(message):
        return message.channel == ctx.author.dm_channel and message.author == ctx.author

    await ctx.author.send('Enter account: ')
    Acc = (await bot.wait_for('message', check=check, timeout=30.0)).content

    await ctx.author.send('Enter password: ')
    Ps = (await bot.wait_for('message', check=check, timeout=30.0)).content

    if (ad['account'][UserIndex] == Acc and ad['password'][UserIndex] == Ps):
        ad['status'][UserIndex] = '1'
        await ctx.author.send('Login Success!')
    else:
        ad['status'][UserIndex] = '0'
        await ctx.author.send('Login Failed.')
        return

    temp_file = open('account_data.json', mode='w', encoding='utf8')
    json.dump(ad, temp_file)
    temp_file.close()

# account logout
@acc.command()
async def logout(ctx):
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

    if (ad['status'][UserIndex] == '0'):
        await ctx.author.send('You\'ve already logout!')
        return

    ad['status'][UserIndex] = '0'
    await ctx.author.send('Logout Success!')

    temp_file = open('account_data.json', mode='w', encoding='utf8')
    json.dump(ad, temp_file)
    temp_file.close()

# register account
@acc.command()
async def register(ctx):
    await ctx.message.delete()
    temp_file = open('account_data.json', mode='r', encoding='utf8')
    ad = json.load(temp_file)  # account data
    temp_file.close()

    for UserId in ad['id']:
        if (str(ctx.author.id) == UserId):
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

    if (RegPs != PsCfm):
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

# account manipulation
@acc.command()
async def mani(ctx):
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
        ad['account'][UserIndex] = MAcc
    if (PsChg == 'yes'):
        ad['password'][UserIndex] = MPs

    await ctx.author.send('Account manipulation success!')

    temp_file = open('account_data.json', mode='w', encoding='utf8')
    json.dump(ad, temp_file)
    temp_file.close()
#===== group - account =====<<


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

#keep_alive.keep_alive()

bot.run(db['TOKEN'])