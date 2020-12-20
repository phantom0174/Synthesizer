import json
import sqlite3
<<<<<<< Updated upstream
=======
import pymongo
from pymongo import MongoClient


client = MongoClient("mongodb+srv://sqcs-bot:xhzwRMtpyso1DNn5@test.5wswq.mongodb.net/SQCS-BOT?retryWrites=true&w=majority")
database = client.syn

>>>>>>> Stashed changes

with open('setting.json', mode='r', encoding='utf8') as jfile:
    db = json.load(jfile)

connection = sqlite3.connect('DataBase.db')
data = connection.cursor()

data.execute("""CREATE TABLE IF NOT EXISTS cadre_apply (
          Id INTEGER,
          Apply_Cadre TEXT,
          Apply_Time TEXT);""")

data.connection.commit()

'''
data.execute("""CREATE TABLE IF NOT EXISTS account (
      Id INTEGER,
      Name TEXT,
      PWD TEXT,
      Status INTEGER);""")

'''