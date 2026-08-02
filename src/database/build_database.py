import sqlite3 as sql
import pandas as pd

connection = sql.connect('../../data/nfl.db')
cursor = connection.cursor()


with open('schema.sql','r') as f:
    contents = f.read()
    cursor.executescript(contents)
    cursor.execute("PRAGMA table_info(schedules)")

    schedule_columns = [row[1] for row in cursor.fetchall()]

    cursor.execute("PRAGMA table_info(team_stats)")
    team_columns = [row[1] for row in cursor.fetchall()]


df_schedules = pd.read_csv('../../data/raw/schedules.csv')
df_team_stats = pd.read_csv('../../data/raw/team_stats.csv')

df_schedules = df_schedules[schedule_columns]
df_team_stats = df_team_stats[team_columns]

df_schedules.to_sql('schedules', con=connection, if_exists='append', index=False)
df_team_stats.to_sql('team_stats', con=connection, if_exists='append', index=False)

connection.commit()
connection.close()