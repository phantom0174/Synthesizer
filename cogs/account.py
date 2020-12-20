from core.classes import Cog_Extension
from core.setup import jdata, client
from discord.ext import commands
import core.functions as func


class Account(Cog_Extension):

    @commands.group()
    async def acc(self, ctx):
        pass

    # check account list
    @acc.command()
    @commands.has_any_role('總召', 'Administrator')
    async def list(self, ctx):

        account_cursor = client["account"]
        accounts = account_cursor.find({})

        account_list = str()

        if accounts is not None:
            for item in accounts:
                account_list += f'Id: {item["_id"]}, Name: {item["name"]}, Password: {item["pw"]}, Status: {item["status"]}\n'
        else:
            account_list = 'None'

        print(account_list)

        await func.getChannel(self.bot, '_Report').send(f'[Command]Group acc - list used by member {ctx.author.id}. {func.now_time_info("whole")}')

    # login
    @acc.command()
    async def login(self, ctx):

        account_cursor = client["account"]
        data = account_cursor.find_one({"_id": ctx.author.id})

        if data is None:
            await ctx.author.send(':exclamation: You havn\'t register yet!')
            return

        if data["status"] == 1:
            await ctx.author.send(':exclamation: You\'ve already login!')
            return

        def check(message):
            return message.channel == ctx.author.dm_channel and message.author == ctx.author

        await ctx.author.send('Enter account: ')
        enter_acc = (await self.bot.wait_for('message', check=check, timeout=30.0)).content

        await ctx.author.send('Enter password: ')
        enter_pw = (await self.bot.wait_for('message', check=check, timeout=30.0)).content

        if data['name'] == enter_acc and data['pw'] == enter_pw:
            account_cursor.update_one({"_id": ctx.author.id}, {"$set": {"status": 1}})
            await ctx.author.send(':white_check_mark: Login Success!')
        else:
            await ctx.author.send(':x: Login Failed.')
            return

        await func.getChannel(self.bot, '_Report').send(f'[Command]Group acc - login used by member {ctx.author.id}. {func.now_time_info("whole")}')

    # logout
    @acc.command()
    async def logout(self, ctx):

        account_cursor = client["account"]
        data = account_cursor.find_one({"_id": ctx.author.id})

        if data is None:
            await ctx.author.send(':exclamation: You havn\'t register yet!')
            return

        if data["status"] == 0:
            await ctx.author.send(':exclamation: You\'ve already logout!')
            return

        account_cursor.update_one({"_id": ctx.author.id}, {"$set": {"status": 0}})
        await ctx.author.send(':white_check_mark: Logout Success!')

        await func.getChannel(self.bot, '_Report').send(f'[Command]Group acc - logout used by member {ctx.author.id}. {func.now_time_info("whole")}')

    # register
    @acc.command()
    async def register(self, ctx):

        account_cursor = client["account"]
        data = account_cursor.find_one({"_id": ctx.author.id})

        if data is not None:
            await ctx.author.send(':exclamation: You\'ve already registered!')
            return

        def check(message):
            return message.channel == ctx.author.dm_channel and message.author == ctx.author

        await ctx.author.send('Set account: ')
        register_name = (await self.bot.wait_for('message', check=check, timeout=30.0)).content

        await ctx.author.send('Set password: ')
        register_pw = (await self.bot.wait_for('message', check=check, timeout=30.0)).content

        await ctx.author.send('Password confirming: ')
        confirm_pw = (await self.bot.wait_for('message', check=check, timeout=30.0)).content

        if register_pw != confirm_pw:
            await ctx.author.send(':exclamation: Two password are not the same, please try again registration.')
            return

        member_account_info = {"_id": ctx.author.id, "name": register_name, "pw": register_pw, "status": 0}
        account_cursor.insert_one(member_account_info)

        await ctx.author.send('Register Success!')

        await func.getChannel(self.bot, '_Report').send(f'[Command]Group acc - register used by member {ctx.author.id}. {func.now_time_info("whole")}')

    # manipulation
    @acc.command()
    async def mani(self, ctx):

        account_cursor = client["account"]
        data = account_cursor.find_one({"_id": ctx.author.id})

        if data is None:
            await ctx.author.send(':exclamation: You havn\'t register yet!')
            return

        mani_acc = str()
        mani_pw = str()

        def check(message):
            return message.channel == ctx.author.dm_channel and message.author == ctx.author

        await ctx.author.send('Do you want to change account?(yes/no): ')
        change_acc = (await self.bot.wait_for('message', check=check, timeout=30.0)).content.lower()
        if change_acc == 'yes':
            await ctx.author.send('Re-set account: ')
            mani_acc = (await self.bot.wait_for('message', check=check, timeout=30.0)).content
        elif change_acc != 'no':
            await ctx.author.send(':exclamation: Invalid syntax!')
            return

        await ctx.author.send('Do you want to change password?(yes/no): ')
        change_pw = (await self.bot.wait_for('message', check=check, timeout=30.0)).content.lower()
        if change_pw == 'yes':
            await ctx.author.send('Re-set password: ')
            mani_pw = (await self.bot.wait_for('message', check=check, timeout=30.0)).content

            await ctx.author.send('Password confirming: ')
            confirm_pw = (await self.bot.wait_for('message', check=check, timeout=30.0)).content

            if mani_pw != confirm_pw:
                await ctx.author.send(':exclamation: Two password are not the same, please try again account manipulation.')
                return
        elif change_pw != 'no':
            await ctx.author.send(':exclamation: Invalid syntax!')
            return

        if change_acc == 'yes':
            account_cursor.update_one({"_id": ctx.author.id}, {"$set": {"name": mani_acc}})
        if change_pw == 'yes':
            account_cursor.update_one({"_id": ctx.author.id}, {"$set": {"name": mani_pw}})

        await ctx.author.send(':white_check_mark: Account manipulation success!')

        await func.getChannel(self.bot, '_Report').send(f'[Command]Group acc - mani used by member {ctx.author.id}. {func.now_time_info("whole")}')


def setup(bot):
    bot.add_cog(Account(bot))
