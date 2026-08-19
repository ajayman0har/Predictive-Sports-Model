import sqlite3 as sql
import pandas as pd
import numpy as np
import xgboost as xgb
import pickle as pkl


def build_data():
    pd.options.display.max_columns = None
    connection = sql.connect('../../data/nfl.db')






    game_features_df = pd.read_sql_query("SELECT * FROM game_features", connection)

    #dropping games with ties
    mask = game_features_df['result'] != 0
    game_features_df = game_features_df[mask]

    game_features_df['home_win'] = np.where(game_features_df['result'] > 0, 1, 0)

    feature_columns = [col for col in game_features_df.columns if 'rolling_' in col]

    feature_columns.extend(['season','week','weekday','home_rest','away_rest','spread_line','total_line','home_moneyline','away_moneyline','under_odds','over_odds'])

    #splitting test and train data into dataframes
    mask = game_features_df['season'] < 2025
    train_df = game_features_df[mask]

    mask = game_features_df['season'] == 2025
    test_df = game_features_df[mask]

    #prepping data for training
    X_train = train_df[feature_columns]
    Y_train = train_df['home_win']

    X_test = test_df[feature_columns]
    Y_test = test_df['home_win']

    #changing weekday type to be read by xgboost
    X_train['weekday'] = X_train['weekday'].astype('category')
    X_test['weekday'] = X_test['weekday'].astype('category')
    connection.close()
    return X_train, Y_train , X_test, Y_test, test_df, game_features_df


def train_model(X_train,Y_train):
    #fitting to XGBoost
    model = xgb.XGBClassifier(missing = -1000, enable_categorical=True)
    model.fit(X_train, Y_train)

    with open('pred_model.pkl', 'wb') as f:
        pkl.dump(model, f)

def main():
    X_train, Y_train, X_test, Y_test, test_df, game_features_df = build_data()
    train_model(X_train,Y_train)


if __name__ == '__main__':
    main()