from core.classes import Cog_Extension
from core.setup import jdata, client, link, Score_Board
import core.functions as func
from discord.ext import tasks, commands
from pymongo import MongoClient


class Task(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sb_update.start()

    @tasks.loop(minutes=10)
    async def sb_update(self):
        await self.bot.wait_until_ready()
        print('entered!')
        Score_Board.clear()

        fluctlight_client = MongoClient(link)["LightCube"]
        fluctlight_cursor = fluctlight_client["light-cube-info"]

        data = fluctlight_cursor.find({"deep_freeze": {"$eq": 0}}, {"score": 1}, sort=[("score", -1)])

        for member in data:
            member_name = (await self.bot.guilds[0].fetch_member(member["_id"])).nick
            if member_name is None:
                member_name = (await self.bot.guilds[0].fetch_member(member["_id"])).name

            Score_Board.append([member_name, member["score"]])


def setup(bot):
    bot.add_cog(Task(bot))
