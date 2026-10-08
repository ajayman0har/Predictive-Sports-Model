import pandas as pd
import os

def get_log_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, 'pick_history.csv')

def log_new_picks(results_df):
    log_path = get_log_path()

    results_df = results_df.copy()
    keep_columns = ['season', 'week', 'home_team', 'away_team', 'home_prob', 'away_prob',
                    'home_moneyline', 'away_moneyline', 'home_ev', 'away_ev',
                    'predicted_winner', 'ev_pick', 'models_agree']
    results_df = results_df[keep_columns].copy()
    results_df['game_key'] = (
        results_df['season'].astype(str) + '_' +
        results_df['week'].astype(str) + '_' +
        results_df['home_team'] + '_' +
        results_df['away_team']
    )

    if os.path.exists(log_path):
        existing_log = pd.read_csv(log_path)
        new_rows = results_df[~results_df['game_key'].isin(existing_log['game_key'])]
    else:
        existing_log = pd.DataFrame()
        new_rows = results_df

    if len(new_rows) > 0:
        updated_log = pd.concat([existing_log, new_rows], ignore_index=True)
        updated_log.to_csv(log_path, index=False)
        print(f"Logged {len(new_rows)} new picks.")
    else:
        print("No new picks to log.")


if __name__ == '__main__':
    from src.live.prepare_dashboard import main as get_dashboard_results
    results_df = get_dashboard_results()
    log_new_picks(results_df)