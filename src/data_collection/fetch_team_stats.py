import nflreadpy as nfl
import polars as pl
import os

def fetch_team_stats(years):
    team_stats = nfl.load_team_stats(years)
    team_stats.write_csv("../../data/raw/team_stats.csv")

if __name__ == '__main__':
    years = list(range(2021, 2026))
    fetch_team_stats(years)

