import sqlite3 as sql

connection = sql.connect('../data/nfl.db')
cursor = connection.cursor()
cursor.execute("SELECT COUNT(*) FROM schedules")
print(cursor.fetchall())

cursor.execute("SELECT COUNT(*) FROM team_stats")
print(cursor.fetchall())

connection.close()
