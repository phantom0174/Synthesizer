from core.classes import Cog_Extension
from core.setup import jdata, client
from discord.ext import commands
import core.functions as func


class UW(Cog_Extension):

    @commands.group()
    async def loc(self):
        pass

    @loc.command()
    @commands.has_any_role('總召', 'Administrator')
    async def insert(self, ctx, location_id: str, location_name: str):
        location_cursor = client["location_index"]

        location_info = {"_id": location_id, "name": location_name, "connect": []}
        location_cursor.insert_one(location_info)
        await ctx.send(f'Location {location_name}({location_id}) has been inserted!')

    @loc.command()
    @commands.has_any_role('總召', 'Administrator')
    async def connect(self, ctx, location1_id: str, location2_id: str):
        location_cursor = client["location_index"]

        location1_name = location_cursor.find_one({"_id": location1_id})["name"]
        location2_name = location_cursor.find_one({"_id": location2_id})["name"]

        location_cursor.update({"_id": location1_id}, {"$push": {"connect": location2_id}})
        location_cursor.update({"_id": location2_id}, {"$push": {"connect": location1_id}})

        await ctx.send(f'Location {location1_name} and location {location2_name} has been connected!')

    @loc.command()
    @commands.has_any_role('總召', 'Administrator')
    async def disconnect(self, ctx, location1_id: str, location2_id: str):
        location_cursor = client["location_index"]

        location1_name = location_cursor.find_one({"_id": location1_id})["name"]
        location2_name = location_cursor.find_one({"_id": location2_id})["name"]

        try:
            location_cursor.update({"_id": location1_id}, {"$pop": {"connect": location2_id}})
            location_cursor.update({"_id": location2_id}, {"$pop": {"connect": location1_id}})

            await ctx.send(f'Location {location1_name} and location {location2_name} has been disconnected!')
        except:
            await ctx.send(f'There\'s no connection between location {location1_name} and location {location2_name}!')


def setup(bot):
    bot.add_cog(UW(bot))