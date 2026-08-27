from datetime import datetime, timezone, timedelta
import requests
import pandas as pd
import os
from dotenv import load_dotenv
import ast
import json

#setting week one
anchor = datetime.strptime('2026-09-10T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)



load_dotenv()
API_KEY = os.getenv('API_KEY')
url = "https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds"
params = {'regions': "us",
        "markets": "h2h,spreads,totals",
        "oddsFormat": "american",
        "api_key": API_KEY}

#grabbing the raw data
def fetch_data():
    response = requests.get(url, params=params)
    live_dict = response.json()
    return live_dict

#adding a week row converting datetime to NFL week
def process_week(live_dict):
    live_df = pd.DataFrame(live_dict)
    live_df['week'] = live_df.apply(get_week, axis=1)
    return live_df

#logic to make Week row
def get_week(row):
    game_time = datetime.strptime(row['commence_time'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
    days_since_anchor = (game_time - anchor).days
    week = days_since_anchor // 7 + 1
    return week

#grabbing current NFL week to subsample data
def get_current_week():
    now = datetime.now(timezone.utc)
    days_since_anchor = (now - anchor).days
    week = days_since_anchor // 7 + 1
    if week < 1:
        week = 1
    return week

#masking dataframe to only this weeks games
def this_weeks_games(live_df, current_week):
    mask = live_df['week'] == current_week
    current_week_df = live_df[mask]
    return current_week_df

#grabbing Draftkings odd for both home and away team
def fetch_dk_odds(row):
    for bookmaker in row['bookmakers']:
        if bookmaker['key'] == 'draftkings':
            for market in bookmaker['markets']:
                if market['key'] == 'h2h':
                    return market['outcomes']

    return None


def main():

    #if data doesn't exist in storage, build the data
    try:
        with open('live_odds_raw.json', 'r') as f:
            live_dict = json.load(f)
    except FileNotFoundError:
        live_dict = fetch_data()
        with open('live_odds_raw.json','w') as f:
            json.dump(live_dict, f)

    live_df = process_week(live_dict)

    current_week = get_current_week()

    current_week_df = this_weeks_games(live_df, current_week)

    current_week_df['odds'] = current_week_df.apply(fetch_dk_odds, axis=1)

    return current_week_df


if __name__ == '__main__':
    result = main()
    print(result[['home_team', 'away_team','commence_time','week','bookmakers','odds']])
    print(f'Number of games this week: {len(result)}')