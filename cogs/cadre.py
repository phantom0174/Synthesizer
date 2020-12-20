from discord.ext import commands
from core.classes import Cog_Extension
from core.setup import jdata, client
import core.functions as func


class Cadre(Cog_Extension):

    @commands.group()
    async def ca(self, ctx):
        pass

    @ca.command()
    async def apply(self, ctx, cadre):
        if ctx.channel.id != 774794670034124850:
            return

        applicant = ctx.author.id
        if func.cadre_trans(cadre) == -1:
            await ctx.send(f':exclamation: There are no cadre called {cadre}!')
            return

        cadre_cursor = client["cadre"]
        data = cadre_cursor.find_one({"_id": applicant})

        if data is not None:
            await ctx.author.send(f':exclamation: You\'ve already made a application!\n'
                                  f'Id: {data["_id"]}, Apply Cadre: {data["apply_cadre"]}, Apply Time: {data["apply_time"]}')
            return

        apply_time = func.now_time_info('whole')
        apply_info = {"_id": applicant, "apply_cadre": cadre, "apply_time": apply_time}
        cadre_cursor.insert_one(apply_info)

        await ctx.send(f':white_check_mark: Application committed!\n'
                       f'Id: {applicant}, Apply Cadre: {cadre}, Apply Time: {apply_time}')

        await func.getChannel(self.bot, '_Report').send(
            f'[Command]Group ca - apply used by member {applicant}. {func.now_time_info("whole")}')

    @ca.command()
    @commands.has_any_role('總召', 'Administrator')
    async def list(self, ctx):

        cadre_cursor = client["cadre"]
        data = cadre_cursor.find({})

        apply_info = str()
        for item in data:
            member_name = await self.bot.guilds[0].fetch_member(item["_id"])
            if member_name is None:
                member_name = await self.bot.fetch_user(item["_id"])

            apply_info += f'{member_name}: {item["apply_cadre"]}, {item["apply_time"]}\n'

        if len(apply_info) == 0:
            apply_info = ':exclamation: There are no application!'

        await ctx.author.send(apply_info)

        await func.getChannel(self.bot, '_Report').send(
            f'[Command]Group ca - list used by member {ctx.author.id}. {func.now_time_info("whole")}')

    @ca.command()
    @commands.has_any_role('總召', 'Administrator')
    async def permit(self, ctx, permit_id: int):

        cadre_cursor = client["cadre"]
        data = cadre_cursor.find_one({"_id": permit_id})

        if data is None:
            await ctx.send(f':exclamation: There are no applicant whose id is {permit_id}!')
            return

        apply_role = func.cadre_trans(data["apply_cadre"])
        cadre_role = ctx.guild.get_role(jdata['cadre_id'][apply_role])

        member = await ctx.guild.fetch_member(data["_id"])
        await member.add_roles(cadre_role)

        await ctx.author.send(
            f':white_check_mark: You\'ve permitted user {member.name} to join cadre {data["apply_cadre"]}!')
        await member.send(f':white_check_mark: You\'ve been permitted to join cadre {data["apply_cadre"]}!')

        cadre_cursor.delete_one({"_id": data["_id"]})

        await func.getChannel(self.bot, '_Report').send(
            f'[Command]Group ca - permit used by member {ctx.author.id}. {func.now_time_info("whole")}')

    @ca.command()
    @commands.has_any_role('總召', 'Administrator')
    async def search(self, ctx, search_id: int):

        cadre_cursor = client["cadre"]
        data = cadre_cursor.find_one({"_id": search_id})

        if data is None:
            await ctx.send(f':exclamation: There are no applicant whose Id is {search_id}!')
            return

        member = await ctx.guild.fetch_member(data["_id"])
        await ctx.send(f'{member.name}: {data["apply_cadre"]}, {data["apply_time"]}')

        await func.getChannel(self.bot, '_Report').send(
            f'[Command]Group ca - search used by member {ctx.author.id}. {func.now_time_info("whole")}')

    # department role update
    @commands.command()
    async def role_update(self, ctx, *, msg):
        update_cadre = msg.split(' ')[0]

        school_name_list = msg.split(' ')[1].split('\n')

        if len(school_name_list) % 2 != 0:
            await ctx.send(':exclamation: School -> Name map quantity error!')
            return

        apply_role = func.cadre_trans(update_cadre)
        new_role = ctx.guild.get_role(jdata['cadre_id'][apply_role])

        school = school_name_list[0:len(school_name_list)/2 - 1]
        name = school_name_list[len(school_name_list)/2::]

        for (member_school, member_name) in zip(school, name):
            for member in ctx.guild.members:
                if member.nick is None:
                    continue

                if member_school in member.nick.split(' '):
                    if member_name in member.nick.split(' '):
                        await member.add_role(new_role)
                        await ctx.channel.send(f':white_check_mark: {member.nick}\'s role was updated to {new_role}!')

        await ctx.send(':white_check_mark: Role update complete!')

        await func.getChannel(self.bot, '_Report').send(
            f'[Command]role_update used by member {ctx.author.id}. {func.now_time_info("whole")}')


def setup(bot):
    bot.add_cog(Cadre(bot))
