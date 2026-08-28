from fetch_live_odds import *
import pandas as pd
import numpy as np
from src.features.build_features import get_rolling_team_stats
from src.live.fetch_live_odds import main as fetch_live_odds


def get_latest_stats():
    team_stats_df = get_rolling_team_stats()
    latest_stats = team_stats_df.sort_values(['season','week']).groupby('team').tail(1)
    return latest_stats

def build_live_features():
    live_df = fetch_live_odds()
    latest_stats = get_latest_stats()

    live_df = live_df.merge(latest_stats, how='left',left_on='away_team',right_on='team', suffixes=('','_away') )
    live_df = live_df.merge(latest_stats, how='left', left_on='home_team', right_on='team', suffixes=('', '_home'))

    return live_df


if __name__ == '__main__':
    result = build_live_features()
    print(result.columns.tolist())