import sqlite3 as sql
import pandas as pd
import os

def get_db_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, '..', '..', 'data', 'nfl.db')

def build_features():
    pd.options.display.max_columns = None
    connection = sql.connect(get_db_path())

    schedules_df = pd.read_sql_query("SELECT * FROM schedules", connection)
    team_stats_df = get_rolling_team_stats()

    merged_df = schedules_df.merge(team_stats_df, how='left', left_on=['away_team','season','week'],right_on=['team','season','week'])
    merged_df = merged_df.merge(team_stats_df, how='left', left_on=['home_team','season','week'],right_on=['team','season','week'],suffixes=('_home','_away'))

    merged_df = merged_df.drop(columns = ['opponent_team_away','game_id_y','opponent_team_home','game_id','team_home','team_away'])
    merged_df = merged_df.rename(columns ={'game_id_x':'game_id'})

    merged_df.to_sql('game_features', connection, if_exists='replace', index=False)

    connection.close()
    print('sucessfully built features')


def get_rolling_team_stats():
    connection = sql.connect(get_db_path())
    team_stats_df = pd.read_sql_query("SELECT * FROM team_stats", connection)
    connection.close()

    team_stats_df = team_stats_df.sort_values(by=['team', 'season', 'week'])

    stat_columns = ['passing_yards', 'passing_tds', 'passing_interceptions', 'passing_epa', 'passing_cpoe', 'passing_40',
                'rushing_yards', 'rushing_tds', 'rushing_epa', 'rushing_40',
                'receiving_yards', 'receiving_tds', 'receiving_epa', 'receiving_40', 'receiving_yards_after_catch',
                'sack_fumbles_lost', 'rushing_fumbles_lost', 'receiving_fumbles_lost',
                'def_sacks', 'def_interceptions', 'def_tds', 'def_tackles_for_loss',
                'fg_made', 'fg_att', 'pat_pct']

    for i in stat_columns:
        team_stats_df[f'rolling_{i}'] = team_stats_df.groupby('team')[i].transform(
            lambda x: x.shift(periods=1).rolling(window=5, min_periods=1).mean())
        team_stats_df[f'rolling_{i}_missing'] = team_stats_df[f'rolling_{i}'].isna()
        team_stats_df[f'rolling_{i}'] = team_stats_df[f'rolling_{i}'].fillna(-1000)

    return team_stats_df


if __name__ == '__main__':
    build_features()