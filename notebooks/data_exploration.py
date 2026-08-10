import sqlite3 as sql
import pandas as pd
pd.options.display.max_columns = None
connection = sql.connect('../data/nfl.db')

cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM game_features")

print(cursor.fetchall())

connection.close()
