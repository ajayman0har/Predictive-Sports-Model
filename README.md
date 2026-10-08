# NFL Win Probability & EV Model

An end-to-end system that predicts NFL win probabilities, compares them against live sportsbook odds to identify potential value, and tracks performance on a rolling weekly basis throughout the season.

**Status: active / ongoing.** This isn't a one-off project — it runs weekly during the NFL season, logging its own predictions for later evaluation, and is being incrementally improved (see [Roadmap](#roadmap--current-work) below).

---

## What it does

1. Pulls 5 seasons of historical NFL game, team-stat, and schedule data
2. Engineers ~110 features per game, including leakage-safe rolling team performance, situational factors (rest days, weekday), market odds, and a custom Elo rating system
3. Trains a gradient-boosted (XGBoost) classifier to predict win probability
4. Calibrates the model's probabilities using Platt scaling, so a "70% confident" prediction actually wins ~70% of the time
5. Converts live sportsbook moneylines into fair, vig-adjusted probabilities and compares them against the model's calibrated output to flag positive expected-value opportunities
6. Pulls this week's live odds and schedule data, generates fresh predictions for upcoming (not-yet-played) games, and logs them for later reconciliation against actual outcomes
7. Surfaces everything in an interactive Tableau dashboard comparing the model's predicted winner against its EV-based recommendation, side by side

---

## Architecture

```
src/
├── data_collection/   # Pulls historical schedules & team stats (nflreadpy)
├── database/          # SQLite schema + database build pipeline
├── features/          # Leakage-safe rolling-average feature engineering + Elo ratings
├── models/            # XGBoost training + Platt-scaling calibration
├── ev/                # Odds conversion, vig removal, expected-value calculation
├── backtest/          # Historical backtest simulation against a held-out season
└── live/              # Live odds API integration, live feature assembly, weekly pick tracking
```

Each stage reads from and writes to a local SQLite database (`nfl.db`) or passes data forward through plain function calls — there's no hidden global state, and every script can be run independently once its upstream dependencies exist.

---

## Key design decisions

- **Leakage prevention is a first-class concern throughout.** Rolling averages only ever look at *prior* games (via an explicit shift before windowing), and the EV calculation only ever uses the model's own probability — never a mix of the model's and the market's beliefs.
- **XGBoost over logistic regression**, chosen specifically because it handles missing data natively and is insensitive to outlier/sentinel values — both of which matter given a deliberate `-1000` missing-value sentinel strategy used throughout feature engineering (paired with explicit "was this missing" flag columns).
- **Calibration, not just accuracy.** A classifier can have good accuracy while still being badly overconfident in its stated probabilities — which is exactly what this project found (and fixed) using a reliability-diagram diagnosis and Platt scaling via `CalibratedClassifierCV`, chosen over isotonic regression specifically due to the dataset's size.
- **A custom Elo rating system**, built from scratch with home-field advantage, margin-of-victory scaling (adapted from FiveThirtyEight's NFL Elo methodology), and season-to-season regression toward the mean — added as a feature alongside rolling stats, not a replacement for them.
- **Containerized with Docker** so the full pipeline runs identically regardless of machine or environment — every file path is resolved relative to the script's own location rather than assuming a specific working directory, which also makes local runs more robust.

---

## Data sources

- [nflreadpy](https://github.com/nflverse/nflreadpy) — historical and upcoming NFL schedules, team-level stats
- [The Odds API](https://the-odds-api.com/) — live sportsbook odds (DraftKings, with FanDuel as a fallback)

---

## Roadmap / current work

- [ ] Validate whether the Elo rating system produces a statistically reliable improvement, or just a favorable single run (requires multiple retrains to assess variance)
- [ ] Incorporate player-level data and injury information as additional features
- [ ] Kelly Criterion bet sizing, layered on top of the current flat-stake backtest
- [ ] A point-margin regression model, compared against the spread market (complementing the current win-probability/moneyline approach)
- [ ] SHAP-based per-prediction feature attribution, surfaced as a natural-language explanation on the dashboard
- [ ] Deploy the containerized pipeline to GCP (Cloud Run Jobs / Cloud Scheduler) for fully automated weekly runs

---

## Notes

This project requires a paid [The Odds API](https://the-odds-api.com/) key to run the live pipeline; historical model training does not require any API access. It's shared here primarily as a portfolio piece — see the code and commit history for the full implementation, including the debugging and design process behind each component.
