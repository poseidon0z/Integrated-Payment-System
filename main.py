import oracledb
import json

import dbfunctions

with open("pass.json") as f:
    pw = json.load(f)["pass"]

connection = oracledb.connect(user="SYSTEM", password=pw, dsn="localhost/xepdb1")

print("Successfully connected to Oracle Database")
cursor = connection.cursor()

dbfunctions.setup(cursor)
