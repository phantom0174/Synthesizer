from core.classes import Cog_Extension
from discord.ext import commands
from functions import *
from core.setup import *
import discord


class Account(Cog_Extension):
    # account main group
    @commands.group()
    async def acc(self, ctx):
        pass

    # check account_list
    @acc.command()
    async def list(self, ctx):
        if not role_check(ctx.author.roles, ['總召']):
            await ctx.send('You can\'t use that command!')
            return

        data.execute('SELECT * FROM account')
        Accs = data.fetchall()

        print(Accs)

        account_info = str()
        for acc in Accs:
            account_info += f'{acc[1]}({acc[0]})<{acc[2]}>: {acc[3]}\n'

        print(account_info)

        await getChannel('_Report').send(f'[Command]Group acc - list used by member {ctx.author.id}. {now_time_info("whole")}')

    # account login
    @acc.command()
    async def login(self, ctx):
        data.execute(f'SELECT * FROM account WHERE Id={ctx.author.id}')
        info = data.fetchall()

        if len(info) == 0:
            await ctx.author.send('You havn\'t register yet!')
            return

        if info[0][3] == 1:
            await ctx.author.send('You\'ve already login!')
            return

        def check(message):
            return message.channel == ctx.author.dm_channel and message.author == ctx.author

        await ctx.author.send('Enter account: ')
        Acc = (await self.bot.wait_for('message', check=check, timeout=30.0)).content

        await ctx.author.send('Enter password: ')
        Ps = (await self.bot.wait_for('message', check=check, timeout=30.0)).content

        if info[0][1] == Acc and info[0][2] == Ps:
            data.execute(f'UPDATE account SET Status=1 WHERE Id={ctx.author.id};')
            await ctx.author.send('Login Success!')
        else:
            await ctx.author.send('Login Failed.')
            return

        data.connection.commit()

        await getChannel('_Report').send(f'[Command]Group acc - login used by member {ctx.author.id}. {now_time_info("whole")}')

    # account logout
    @acc.command()
    async def logout(self, ctx):
        data.execute(f'SELECT * FROM account WHERE Id={ctx.author.id}')
        info = data.fetchall()

        if len(info) == 0:
            await ctx.author.send('You havn\'t register yet!')
            return

        if info[0][3] == 0:
            await ctx.author.send('You\'ve already logout!')
            return

        data.execute(f'UPDATE account SET Status=0 WHERE Id={ctx.author.id};')
        await ctx.author.send('Logout Success!')

        data.connection.commit()

        await getChannel('_Report').send(f'[Command]Group acc - logout used by member {ctx.author.id}. {now_time_info("whole")}')

    # register account
    @acc.command()
    async def register(self, ctx):
        data.execute(f'SELECT * FROM account WHERE Id={ctx.author.id}')
        info = data.fetchall()

        if len(info) != 0:
            await ctx.author.send('You\'ve already registered!')
            return

        def check(message):
            return message.channel == ctx.author.dm_channel and message.author == ctx.author

        await ctx.author.send('Set account: ')
        RegName = (await self.bot.wait_for('message', check=check, timeout=30.0)).content

        await ctx.author.send('Set password: ')
        RegPs = (await self.bot.wait_for('message', check=check, timeout=30.0)).content

        await ctx.author.send('Password confirming: ')
        PsCfm = (await self.bot.wait_for('message', check=check, timeout=30.0)).content

        if RegPs != PsCfm:
            await ctx.author.send('Two password are not the same, please try again registration.')
            return

        # data.execute(f'INSERT INTO account VALUES({ctx.author.id}, {RegName}, {RegPs}, 0);')
        data.execute(
            f'INSERT INTO account (id, Name, PWD, Status) VALUES ("{ctx.author.id}", "{RegName}", "{RegPs}", 0);')

        await ctx.author.send('Register Success!')

        data.connection.commit()

        await getChannel('_Report').send(f'[Command]Group acc - register used by member {ctx.author.id}. {now_time_info("whole")}')

    # account manipulation
    @acc.command()
    async def mani(self, ctx):
        data.execute(f'SELECT * FROM account WHERE Id="{ctx.author.id}"')
        info = data.fetchall()

        print(info)

        if len(info) == 0:
            await ctx.author.send('You havn\'t register yet!')
            return

        MAcc = str()
        MPs = str()

        def check(message):
            return message.channel == ctx.author.dm_channel and message.author == ctx.author

        await ctx.author.send('Do you want to change account?(yes/no): ')
        AccChg = (await self.bot.wait_for('message', check=check, timeout=30.0)).content.lower()
        if AccChg == 'yes':
            await ctx.author.send('Re-set account: ')
            MAcc = (await self.bot.wait_for('message', check=check, timeout=30.0)).content
        elif AccChg != 'no':
            await ctx.author.send('Invalid syntax!')
            return

        await ctx.author.send('Do you want to change password?(yes/no): ')
        PsChg = (await self.bot.wait_for('message', check=check, timeout=30.0)).content.lower()
        if PsChg == 'yes':
            await ctx.author.send('Re-set password: ')
            MPs = (await self.bot.wait_for('message', check=check, timeout=30.0)).content

            await ctx.author.send('Password confirming: ')
            PsCfm = (await self.bot.wait_for('message', check=check, timeout=30.0)).content

            if (MPs != PsCfm):
                await ctx.author.send('Two password are not the same, please try again account manipulation.')
                return
        elif PsChg != 'no':
            await ctx.author.send('Invalid syntax!')
            return

        if AccChg == 'yes':
            data.execute(f'UPDATE account SET Name="{MAcc}" WHERE Id={ctx.author.id};')
        if PsChg == 'yes':
            data.execute(f'UPDATE account SET PWD="{MPs}" WHERE Id={ctx.author.id};')

        await ctx.author.send('Account manipulation success!')

        data.connection.commit()

        await getChannel('_Report').send(f'[Command]Group acc - mani used by member {ctx.author.id}. {now_time_info("whole")}')


def setup(bot):
    bot.add_cog(Account(bot))
