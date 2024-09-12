import pandas as pd

def process_fights_data(input_csv, fight_stats_csv, top50_fights_csv):
    # GETS DATAFRAME FROM CSV
    df = pd.read_csv(input_csv, header='infer', index_col=None)

    # ALLOW PANDAS TO DISPLAY ALL COLUMNS
    pd.set_option('display.max_columns', 100)

    # SELECT NECESSARY COLUMNS ONLY
    df = df[["player_1_team", "player_2_team"]]

    # LISTING DEPRECATED FRANCHISES
    rmv_list = ['Arizona Coyotes', 'Atlanta Thrashers']

    # FILTERING THEM OUT
    df = df[~df['player_1_team'].isin(rmv_list) & ~df['player_2_team'].isin(rmv_list)]

    # SORTING THE COLUMNS TO AVOID DEDUPLICATION BETWEEN SAME TEAMS
    df['team1'], df['team2'] = zip(*df.apply(lambda row: sorted([row['player_1_team'], row['player_2_team']]), axis=1))

    # SELECTING SORTED COLUMNS
    df = df[['team1', 'team2']]

    # CONCATENATING TO FORM CONFRONTATIONS
    df['fight'] = df['team1'] + ' x ' + df['team2']

    # COUNTING UNIQUE FIGHTS
    fight_counts = df['fight'].value_counts().reset_index()

    # RENAMING COLUMNS
    fight_counts.columns = ['fight', 'count']

    # CALCULATING THE PERCENTAGE
    fight_counts['percentage'] = (fight_counts['count'] / fight_counts['count'].sum()) * 100

    # SORTING DESC
    fight_counts = fight_counts.sort_values(by='percentage', ascending=False).reset_index(drop=True)

    # MAKING INDEX START AT 1
    fight_counts.index = fight_counts.index + 1

    # SAVES TO CSV ALL FIGHT HISTORY
    fight_counts.to_csv(fight_stats_csv, index=True)

    # SELECT TOP 50 RIVALRIES
    df_top50 = fight_counts.loc[0:50, :]

    # SAVES TOP 50 TO CSV
    df_top50.to_csv(top50_fights_csv, index=True)

if __name__ == "__main__":
    
    process_fights_data("data/nhl-regular-all-fights.csv", "data/fight_stats.csv", "data/top50_fights.csv")