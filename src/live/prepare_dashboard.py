from src.live.build_live_features import main as get_results
import numpy as np

def add_dashboard_columns(results_df):

    #if home prob over 50 pct, choose home team else choose away
    results_df['predicted_winner'] = np.where(results_df['home_prob']>0.5, results_df['home_team'], results_df['away_team'])

    def get_ev_pick(row):
        if row['home_ev'] >= 0.05:
            return row['home_team']
        elif row['away_ev'] >= 0.05:
            return row['away_team']
        else:
            return 'No Bet'

    results_df['ev_pick'] = results_df.apply(get_ev_pick, axis=1)
    results_df['models_agree'] = results_df['ev_pick'] == results_df['predicted_winner']

    return results_df



def main():
    results_df = get_results()
    results_df = add_dashboard_columns(results_df)
    results_df.to_csv('prediction_model.csv', index=False)
    return results_df


if __name__ == '__main__':
    main()