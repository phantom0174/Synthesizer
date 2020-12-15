import json
import sqlite3

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