from discord.ext import commands
from core.classes import Cog_Extension
from core.setup import *
from core.functions import *


class Cadre(Cog_Extension):

    @commands.group()
    async def ca(self, ctx):
        pass

    @ca.command()
    async def apply(self, ctx, msg):
        if ctx.channel.id != 774794670034124850:
            return

        applicant = ctx.author.id
        if cadre_trans(msg) == -1:
            await ctx.send(f':exclamation: There are no cadre called {msg}!')
            return

        data.execute(f'SELECT * FROM cadre_apply WHERE Id={applicant};')
        info = data.fetchall()

        if len(info) != 0:
            await ctx.send(f':exclamation: You\'ve already made a application!\n'
                           f'Id: {info[0][0]}, Apply Cadre: {info[0][1]}, Apply Time: {info[0][2]}')
            return

        apply_time = now_time_info("whole")
        data.execute(f'INSERT INTO cadre_apply VALUES({applicant}, "{msg}", "{apply_time}");')
        data.connection.commit()

        await ctx.send(f':white_check_mark: Application committed!\n'
                       f'Id: {applicant}, Apply Cadre: {msg}, Apply Time: {apply_time}')

        await getChannel('_Report').send(f'[Command]Group ca - apply used by member {ctx.author.id}. {now_time_info("whole")}')

    @ca.command()
    @commands.has_any_role('總召', 'Administrator')
    async def list(self, ctx):

        data.execute('SELECT * FROM cadre_apply;')
        info = data.fetchall()

        applies = str()
        for apply in info:
            member = await self.bot.fetch_user(apply[0])
            applies += f'{member.name}: {apply[1]}, {apply[2]}\n'

        if len(applies) == 0:
            applies = ':exclamation: There are no application!'

        await ctx.author.send(applies)

        await getChannel('_Report').send(f'[Command]Group ca - list used by member {ctx.author.id}. {now_time_info("whole")}')

    @ca.command()
    @commands.has_any_role('總召', 'Administrator')
    async def permit(self, ctx, msg):

        data.execute(f'SELECT Id, Apply_Cadre FROM cadre_apply WHERE Id={int(msg)};')
        info = data.fetchall()

        if (len(info) == 0):
            await ctx.send(f':exclamation: There are no applicant whose id is {msg}!')
            return

        apply_role = cadre_trans(info[0][1])
        cadre_role = ctx.guild.get_role(db['cadre_id'][apply_role])

        member = await ctx.guild.fetch_member(info[0][0])
        await member.add_roles(cadre_role)

        await ctx.author.send(f':white_check_mark: You\'ve permitted user {info[0][0]} to join cadre {info[0][1]}!')
        await member.send(f':white_check_mark: You\'ve been permitted to join cadre {info[0][1]}!')

        data.execute(f'DELETE FROM cadre_apply WHERE Id={info[0][0]};')
        data.connection.commit()

        await getChannel('_Report').send(f'[Command]Group ca - permit used by member {ctx.author.id}. {now_time_info("whole")}')

    @ca.command()
    @commands.has_any_role('總召', 'Administrator')
    async def search(self, ctx, msg):

        data.execute(f'SELECT * FROM cadre_apply WHERE Id={msg};')
        info = data.fetchall()

        if (len(info) == 0):
            await ctx.send(f':exclamation: There are no applicant whose Id is {msg}!')
            return

        member = await ctx.guild.fetch_member(info[0][0])
        await ctx.send(f'{member.name}: {info[0][1]}, {info[0][2]}')

        await getChannel('_Report').send(f'[Command]Group ca - search used by member {ctx.author.id}. {now_time_info("whole")}')

    # ===== group - cadre application =====<<

    # department role update
    @commands.command()
    async def role_update(self, ctx, *, msg):
        # Mode:: 1:副召, 2:美宣, 3:網管, 4:公關, 5:議程, 6:管理
        print(msg.split(' '))
        if (len(msg.split(' ')) != 2):
            await ctx.send(':exclamation: There are no target selected!')
            return

        mode = int(msg.split(' ')[0])
        print(mode)

        msg_split = msg.split(' ')[1].split('\n')
        print(msg_split)

        if (int(len(msg_split)) % 2 != 0):
            await ctx.send(':exclamation: School -> Name map error!')
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
                        await ctx.channel.send(f':white_check_mark: {member.name}\'s role was updated to {new_role}!')

        await ctx.send(':white_check_mark: Role update complete!')

        await getChannel('_Report').send(f'[Command]role_update used by member {ctx.author.id}. {now_time_info("whole")}')


def setup(bot):
    bot.add_cog(Cadre(bot))
