import sqlite3 as sql
import pandas as pd
import numpy as np
import sklearn
from sklearn.linear_model import LinearRegression
import xgboost as xgb
from sklearn.metrics import accuracy_score , classification_report
from sklearn.calibration import calibration_curve
from sklearn.calibration import CalibratedClassifierCV
import matplotlib.pyplot as plt
import requests

API_KEY = '71986c9f74760a650ebe0cb2e559d0b2'
url = "https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds"
params = {'regions': "us",
          "markets": "h2h,spreads,totals",
          "oddsFormat":"american",
          "api_key": API_KEY}

response = requests.get(url, params=params)
print(response.status_code)
print(response.json())

pd.options.display.max_columns = None
connection = sql.connect('../data/nfl.db')

cursor = connection.cursor()




connection.close()