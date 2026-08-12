import sqlite3 as sql
import pandas as pd
import numpy as np
import sklearn
from sklearn.linear_model import LinearRegression
import xgboost as xgb
from sklearn.metrics import accuracy_score , classification_report
import matplotlib.pyplot as plt

pd.options.display.max_columns = None
connection = sql.connect('../data/nfl.db')

cursor = connection.cursor()




game_features_df = pd.read_sql_query("SELECT * FROM game_features", connection)

#dropping games with ties
mask = game_features_df['result'] != 0
game_features_df = game_features_df[mask]

game_features_df['home_win'] = np.where(game_features_df['result'] > 0, 1, 0)

feature_columns = [col for col in game_features_df.columns if 'rolling_' in col]

feature_columns = [col for col in game_features_df.columns if 'rolling_' in col and '_missing' not in col]

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

#fitting to XGBoost
model = xgb.XGBClassifier(missing = -1000, enable_categorical=True)
model.fit(X_train, Y_train)

predictions = model.predict(X_test)
accuracy = accuracy_score(Y_test, predictions)
print(accuracy)
print(Y_test.mean())
print(classification_report(Y_test, predictions))
probabilities = model.predict_proba(X_test)
print(probabilities[:5])
home_win_probs = probabilities[:, 1]

plt.hist(home_win_probs, bins=20)
plt.show()

connection.close()