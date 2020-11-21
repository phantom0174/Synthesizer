import discord
from discord.ext import commands
import json
import time

with open('database.json', mode='r', encoding='utf8') as jfile:
    db = json.load(jfile)

bot = commands.Bot(command_prefix='sc!')


@bot.event
async def on_ready():
    print("------>> Bot is online <<------")

#ping
@bot.command()
async def ping(ctx):
    await ctx.send(f'{round(bot.latency * 1000)} (ms)')

#check member
@bot.command()
async def m_c(ctx):
    for member in ctx.guild.members:
        print(member)


bot.run(db['TOKEN'])