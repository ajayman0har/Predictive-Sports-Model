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




connection.close()