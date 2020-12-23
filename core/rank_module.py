import math
import core.functions as func
from core.setup import jdata, client, link
from pymongo import MongoClient
import discord


async def get_rank(bot, score, new_mode):
    rank_index = str(int(score / 50))

    mvisualizer_client = MongoClient(link)["mvisualizer"]
    rank_cursor = mvisualizer_client["rank_index"]

    new_rank = rank_cursor.find_one({"_id": new_mode + rank_index})["name"]

    return new_rank
