import nflreadpy as nfl
import polars as pl
import os

def fetch_schedules(years):
    schedules = nfl.load_schedules(years)
    schedules.write_csv("../../data/raw/schedules.csv")

if __name__ == '__main__':
    years = list(range(2021, 2026))
    fetch_schedules(years)
