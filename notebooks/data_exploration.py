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

pd.options.display.max_columns = None
connection = sql.connect('../data/nfl.db')

cursor = connection.cursor()

def moneyline_to_odds(moneyline):
    odds = 0
    if moneyline > 0:
        odds = 100/(moneyline + 100)
    elif moneyline < 0:
        odds = abs(moneyline)/(abs(moneyline)+100)
    else:
        raise ValueError("Moneyline not valid")

    return odds


def find_fair_prob(home_raw_prob,away_raw_prob):
    total = home_raw_prob + away_raw_prob
    home_fair_prob = home_raw_prob/total
    away_fair_prob = away_raw_prob/total
    return home_fair_prob, away_fair_prob

def moneyline_to_payout(moneyline, wager):
    if moneyline > 0:
        return moneyline/100 * wager
    elif moneyline < 0:
        return 100/abs(moneyline) * wager
    else :
        raise ValueError("Moneyline not valid")


def calculate_ev(prob, moneyline,wager):
    payout = moneyline_to_payout(moneyline, wager)
    ev = ((prob * payout)- ((1-prob)*wager))
    return ev

print(calculate_ev(.7,150,1))
raw_odds = moneyline_to_odds(150)
print(cal)
connection.close()