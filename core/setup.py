from pymongo import MongoClient
import pymongo
import json
import os

# database setup
password = os.environ.get("PW")
account = os.environ.get("ACCOUNT")
link = f"mongodb+srv://{account}:{password}@light-cube-cluster.5wswq.mongodb.net/syn?retryWrites=true&w=majority"
client = MongoClient(link).synthesizer

with open('setting.json', mode='r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

Score_Board = list(list())
