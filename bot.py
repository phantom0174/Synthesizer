from discord.ext import commands
from core.setup import *
from functions import *
# import keep_alive
import discord
import asyncio
import sys
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='sc!', intents=intents)

@bot.event
async def on_ready():
    print("------>> Bot is online <<------")
    await setChannel(bot)
    await Auto_task()


async def Auto_task():
    guild = bot.guilds[0]

    AdminRole = guild.get_role(db['Admin'])
    while True:
        if 21 <= now_time_info('hour') <= 23 or 0 <= now_time_info('hour') <= 6:
            data.execute('SELECT Id, Status FROM account')
            Accs = data.fetchall()

            for acc in Accs:
                user = await guild.fetch_member(acc[0])
                if acc[1] == 1:
                    await user.add_roles(AdminRole)
                elif acc[1] == 0:
                    await user.remove_roles(AdminRole)
            await getChannel('_Report').send(f'[Update]Guild logined member admin role. {now_time_info("whole")}')

        await asyncio.sleep(600)


@bot.command()
async def load(ctx, msg):
    try:
        bot.load_extension(f'cogs.{msg}')
        await ctx.send(f'Extension {msg} loaded.')
    except:
        await ctx.send(f'There are no extension called {msg}!')


@bot.command()
async def unload(ctx, msg):
    try:
        bot.unload_extension(f'cogs.{msg}')
        await ctx.send(f'Extension {msg} unloaded.')
    except:
        await ctx.send(f'There are no extension called {msg}!')


@bot.command()
async def reload(ctx, msg):
    try:
        bot.reload_extension(f'cogs.{msg}')
        await ctx.send(f'Extension {msg} reloaded.')
    except:
        await ctx.send(f'There are no extension called {msg}!')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and filename != 'setup.py':
        bot.load_extension(f'cogs.{filename[:-3]}')


@bot.command()
async def safe_stop(ctx):
    if not role_check(ctx.author.roles, ['總召']):
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


# keep_alive.keep_alive()

bot.run(os.environ.get("TOKEN"))
