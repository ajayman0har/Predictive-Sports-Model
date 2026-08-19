from src.ev.odds_utils import moneyline_to_payout
import pickle
from src.models.train_model import build_data
import pandas as pd


def calculate_ev(prob, moneyline,wager):
    payout = moneyline_to_payout(moneyline, wager)
    ev = ((prob * payout)- ((1-prob)*wager))
    return ev

def load_model():
    with open ("../models/calibrated_pred_model.pkl", "rb") as f:
        calibrated_model = pickle.load(f)
    return calibrated_model

def load_data():
    X_train, Y_train, X_test, Y_test, test_df, game_features_df = build_data()
    return X_test,test_df, game_features_df

def ev_check(calibrated_model,X_test,test_df):

    ev_results = []
    for i, row in X_test.iterrows():
        prob = calibrated_model.predict_proba(X_test.loc[[i]])
        prob_home = prob[0][1]
        prob_away = 1-prob_home
        home_ml = row['home_moneyline']
        away_ml = row['away_moneyline']

        home_ev = calculate_ev(prob_home, home_ml, wager=1)
        away_ev = calculate_ev(prob_away, away_ml, wager=1)

        ev_results.append({
            'game_id': test_df.loc[i,'game_id'],
            'home_ev': home_ev,
            'away_ev': away_ev,
            'home_prob':prob_home,
            'away_prob':prob_away,
        })
    ev_df = pd.DataFrame(ev_results)
    return ev_df

def main():
    calibrated_model = load_model()
    X_test, test_df,game_features_df = load_data()
    ev_df = ev_check(calibrated_model,X_test,test_df)
    ev_df.to_csv('ev.csv')

if __name__ == '__main__':
    main()