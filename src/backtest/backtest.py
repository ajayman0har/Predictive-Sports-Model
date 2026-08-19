from src.ev.calculate_ev import *
from src.models.train_model import build_data
import matplotlib.pyplot as plt


def backtest(ev_df, test_df):
    backtest_df = ev_df.merge(test_df[['game_id', 'home_win','home_moneyline','away_moneyline','season','week']], on='game_id', how='left')
    return backtest_df

def decide_bet(row):
    if row['home_ev'] >= 0.05:
        return 'home'
    elif row['away_ev'] >= 0.05:
        return 'away'
    else:
        return None

def deciding(backtest_df):
    backtest_df['bet_on'] = backtest_df.apply(decide_bet, axis=1)
    return backtest_df

def did_bet_win(row):
    if row['bet_on'] == 'home' and row['home_win'] == 1:
        return 1
    elif row['bet_on'] == 'away' and row['home_win'] == 1:
        return 0
    elif row['bet_on'] == 'home' and row['home_win'] == 0:
        return 0
    elif row['bet_on'] == 'away' and row['home_win'] == 0:
        return 1
    return None

def calculate_profits(row):
    if pd.isna(row['bet_on']):
        return 0
    elif row['Win'] ==1:
        moneyline = row['home_moneyline'] if row['bet_on'] == 'home' else row['away_moneyline']
        return moneyline_to_payout(moneyline, wager=1)
    else:
        return -1

def main():
    calibrated_model = load_model()
    X_test, test_df, game_features_df = load_data()
    ev_df = ev_check(calibrated_model, X_test, test_df)
    backtest_df = backtest(ev_df, test_df)
    backtest_df = deciding(backtest_df)
    backtest_df['Win'] = backtest_df.apply(did_bet_win, axis=1)
    backtest_df['profits'] = backtest_df.apply(calculate_profits, axis=1)
    backtest_df = backtest_df.sort_values(by=['season','week'])
    backtest_df['cumulative_profit'] = backtest_df['profits'].cumsum()

    print(backtest_df[['game_id', 'home_ev', 'away_ev', 'bet_on', 'home_win', 'Win', 'profits', 'home_moneyline',
                       'away_moneyline']].head(10))
    print(backtest_df['bet_on'].isna().sum())
    skipped = backtest_df[backtest_df['bet_on'].isna()]
    print((skipped['profits'] == -1).sum())

    plt.plot(backtest_df['cumulative_profit'].values)
    plt.xlabel('Bet No.')
    plt.ylabel('Profit')
    plt.title('Cumulative Profit')
    plt.show()



if __name__ == "__main__":
    main()