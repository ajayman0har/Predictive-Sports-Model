import pandas as pd
import sqlite3
import math

home_adv = 65
k = 20

def compute_elo_ratings():
    connection = sqlite3.connect("../../data/nfl.db")  # creates file if it doesn't exist
    schedules_df = pd.read_sql("SELECT * FROM schedules", connection)
    connection.close()

    schedules_df = schedules_df.sort_values(by=['season','week'])
    #drop ties
    schedules_df = schedules_df[schedules_df['result'] !=0]

    current_elo = {}

    elo_records = []
    previous_season = None


    for index, row in schedules_df.iterrows():

        current_season = row['season']

        if previous_season is not None and current_season != previous_season:
            for team in current_elo:
                current_elo[team] = 0.75 * current_elo[team] + .25 * 1500


        previous_season = current_season



        home_team = row['home_team']
        away_team = row['away_team']


        home_rating = current_elo.get(home_team,1500)
        away_rating = current_elo.get(away_team,1500)


        elo_records.append({
            'game_id': row['game_id'],
            'home_elo_pregame': home_rating,
            'away_elo_pregame': away_rating,
        })


        expected_home = 1 / (1+10**((away_rating-(home_rating+home_adv))/400))
        actual_home = 1 if row['result'] > 0 else 0

        home_score = row['home_score']
        away_score = row['away_score']

        margin = abs(home_score - away_score)

        #scales elo change based on blowouts

        if home_score > away_score:
            winner_elo_diff = (home_rating + home_adv) - away_rating
        else:
            winner_elo_diff = (away_rating) - (home_rating + home_adv)

        margin_multiplier = math.log(margin + 1) * (2.2 / (winner_elo_diff * 0.001 + 2.2))

        new_home_rating = home_rating + k * margin_multiplier * (actual_home - expected_home)
        new_away_rating = away_rating + k * margin_multiplier *((1-actual_home)-(1-expected_home))


        current_elo[home_team] = new_home_rating
        current_elo[away_team] = new_away_rating


    elo_df = pd.DataFrame(elo_records)
    return elo_df, current_elo


if __name__ == '__main__':
    elo_df, current_elo = compute_elo_ratings()
    print(elo_df.head(20))
    print(elo_df['home_elo_pregame'].describe())