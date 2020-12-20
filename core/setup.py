import json
import pymongo
from pymongo import MongoClient

# database setup
link = "mongodb+srv://bot-console:XgZLiNW33wrY6tqi@light-cube-cluster.5wswq.mongodb.net/syn?retryWrites=true&w=majority"
client = pymongo.MongoClient(link).Synthesizer

with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)
