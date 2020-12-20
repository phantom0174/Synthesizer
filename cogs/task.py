from core.setup import jdata, client
import core.functions as func
from discord.ext import tasks
from core.classes import Cog_Extension


class Task(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.admin_check.start()

    @tasks.loop(minutes=10)
    async def admin_check(self):
        await self.bot.wait_until_ready()
        if 21 <= func.now_time_info('hour') <= 23 or 0 <= func.now_time_info('hour') <= 6:
            admin_role = self.bot.guilds[0].get_role(jdata['Admin'])

            account_cursor = client["account"]
            accounts = account_cursor.find({})

            for item in accounts:
                user = await self.bot.guilds[0].fetch_member(item["_id"])
                if item["status"] == 1:
                    await user.add_roles(admin_role)
                elif item["status"] == 0:
                    await user.remove_roles(admin_role)
            await func.getChannel(self.bot, '_Report').send(f'[Update]Admin role. {func.now_time_info("whole")}')


def setup(bot):
    bot.add_cog(Task(bot))
