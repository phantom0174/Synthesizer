from core.classes import Cog_Extension
from core.setup import jdata, client
import core.functions as func
from discord.ext import tasks, commands


class Task(Cog_Extension):
    @commands.command()
    async def none(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Task(bot))
