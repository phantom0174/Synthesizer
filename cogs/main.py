from core.classes import Cog_Extension
from discord.ext import commands


class Main(Cog_Extension):
    # ping
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f':stopwatch: {round(self.bot.latency * 1000)} (ms)')

    # check member
    @commands.command()
    @commands.has_any_role('總召', 'Administrator')
    async def m_c(self, ctx):
        for member in ctx.guild.members:
            print(member)


def setup(bot):
    bot.add_cog(Main(bot))
