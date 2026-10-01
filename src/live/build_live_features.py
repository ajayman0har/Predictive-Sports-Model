from fetch_live_odds import *
import pandas as pd
import numpy as np
from src.features.build_features import get_rolling_team_stats
from src.live.fetch_live_odds import main as fetch_live_odds
import nflreadpy as nfl
import polars as pl
import pickle as pkl
from src.ev.calculate_ev import calculate_ev
from src.features.build_elo import compute_elo_ratings as elo



def get_upcoming_schedule():
    schedules_df = nfl.load_schedules([2026])
    schedules_df = schedules_df.select(['home_team','away_team','season','week','weekday','home_rest', 'away_rest','spread_line','total_line', 'under_odds', 'over_odds'])
    schedules_df = schedules_df.to_pandas()
    return schedules_df

def get_latest_stats():
    team_stats_df = get_rolling_team_stats()
    latest_stats = team_stats_df.sort_values(['season','week']).groupby('team').tail(1)
    return latest_stats

def build_live_features():

    live_df = fetch_live_odds()
    latest_stats = get_latest_stats()

    away_stats = latest_stats.add_suffix('_away')
    home_stats = latest_stats.add_suffix('_home')

    live_df = live_df.merge(home_stats, how='left', left_on='home_team', right_on='team_home')
    live_df = live_df.merge(away_stats, how='left', left_on='away_team', right_on='team_away')

    elo_df , current_elo = elo()
    current_elo_df = pd.DataFrame(list(current_elo.items()), columns=['team', 'elo'])

    away_elo = current_elo_df.add_suffix('_away').rename(columns={'team_away': 'elo_team_away'})
    home_elo = current_elo_df.add_suffix('_home').rename(columns={'team_home': 'elo_team_home'})

    live_df = live_df.merge(home_elo, how='left', left_on='home_team', right_on='elo_team_home')
    live_df = live_df.merge(away_elo, how='left', left_on='away_team', right_on='elo_team_away')

    #renaming to fit model
    live_df = live_df.rename(columns={'elo_home': 'home_elo_pregame', 'elo_away': 'away_elo_pregame'})

    return live_df

def merge_schedules(live_df):
    schedules_df = get_upcoming_schedule()
    live_df = live_df.merge(schedules_df, how='left', on=['home_team','away_team','week'])
    return live_df

def clean_df(live_df):
    live_df = live_df.drop(columns = ['team_away','team_home', 'game_id_away','game_id_home','opponent_team_away','opponent_team_home'
                            ,'season_home','season_away','id','sport_key','sport_title','commence_time','bookmakers','odds'])
    live_df = live_df.rename(columns={"home_odds": "home_moneyline", "away_odds": "away_moneyline"})

    team_info = live_df[['home_team','away_team','home_moneyline','away_moneyline']].copy()

    feature_columns = [col for col in live_df if 'rolling_' in col]
    feature_columns.extend(['season','week','weekday','home_rest','away_rest','spread_line',
                           'total_line','home_moneyline','away_moneyline', 'under_odds', 'over_odds','home_elo_pregame','away_elo_pregame'])
    live_df = live_df[feature_columns]
    return live_df, team_info

def predict_live_games(live_game_df):
    live_game_df['weekday'] = live_game_df['weekday'].astype('category')

    with open("../models/calibrated_pred_model.pkl", "rb") as f:
        model = pkl.load(f)

    probabilities = model.predict_proba(live_game_df)
    live_game_df['home_prob'] = probabilities[:,1]
    live_game_df['away_prob'] = 1-live_game_df['home_prob']

    live_game_df['home_ev'] = live_game_df.apply(lambda row: calculate_ev(row['home_prob'], row['home_moneyline'],wager=1), axis=1)
    live_game_df['away_ev'] = live_game_df.apply(lambda row: calculate_ev(row['away_prob'], row['away_moneyline'], wager=1), axis=1)

    return live_game_df


def main():
    live_df = build_live_features()
    live_df = merge_schedules(live_df)
    live_game_df, team_info = clean_df(live_df)
    live_game_df = predict_live_games(live_game_df)
    results_df = pd.concat([live_game_df,team_info],axis=1)
    print(results_df[['home_team','away_team','home_prob', 'away_prob', 'home_moneyline', 'away_moneyline', 'home_ev', 'away_ev']])
    return results_df

if __name__ == '__main__':
    main()
