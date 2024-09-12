import json
import os 
import pandas as pd
from datetime import timedelta

def transform(json_path: str,tz: int ,csv_output: str):
    """
    Transforms json files into single csv file containing all data and fixing datetime if needed
    """
    # LOADS JSON

    # LIST OUTSIDE THE LOOP TO HOLD ALL GAME DATA
    games_list = []

    for file_name in [file for file in os.listdir(json_path) if file.endswith('.json')]:
        with open(json_path + file_name) as file:

            data = json.load(file)

        # EXTRACTING GAMES LIST
        game_weeks = data.get('gameWeek', [])

        # LOOP THROUGH GAMES IN GAME WEEKS
        for game_week in game_weeks:
            games = game_week.get('games', [])   
            # LOOP THOUGH EVERY GAME
            for game in games:
                game_data = {
                    'data': game.get('startTimeUTC'),
                    'Away Team': game.get('awayTeam', {}).get('placeName', {}).get('default', ''),
                    'Home Team': game.get('homeTeam', {}).get('placeName', {}).get('default', '')
                }
                games_list.append(game_data)

    df = pd.DataFrame(games_list)

    # REORGANIZE COLUMNS
    df = df[['data', 'Away Team', 'Home Team']]

    # MAKE DATETIME COLUMN
    df['data'] = pd.to_datetime(df['data'], format='%Y-%m-%dT%H:%M:%SZ')
    
    # FIX TIMEZONE
    df['data'] = df['data'] + timedelta(hours=tz)

    # RENAME FRANCHISES
    team_map = {
        "Anaheim": "Anaheim Ducks",
        "Utah": "Utah HC",
        "Boston": "Boston Bruins",
        "Buffalo": "Buffalo Sabres",
        "Calgary": "Calgary Flames",
        "Carolina": "Carolina Hurricanes",
        "Chicago": "Chicago Blackhawks",
        "Colorado": "Colorado Avalanche",
        "Columbus": "Columbus Blue Jackets",
        "Dallas": "Dallas Stars",
        "Detroit": "Detroit Red Wings",
        "Edmonton": "Edmonton Oilers",
        "Florida": "Florida Panthers",
        "Los Angeles": "Los Angeles Kings",
        "Minnesota": "Minnesota Wild",
        "Montréal": "Montreal Canadiens",
        "Nashville": "Nashville Predators",
        "New Jersey": "New Jersey Devils",
        "New York": "New York Rangers",
        "New York Islanders": "New York Islanders",
        "Ottawa": "Ottawa Senators",
        "Philadelphia": "Philadelphia Flyers",
        "Pittsburgh": "Pittsburgh Penguins",
        "San Jose": "San Jose Sharks",
        "Seattle": "Seattle Kraken",
        "St. Louis": "St. Louis Blues",
        "Tampa Bay": "Tampa Bay Lightning",
        "Toronto": "Toronto Maple Leafs",
        "Vancouver": "Vancouver Canucks",
        "Vegas": "Vegas Golden Knights",
        "Washington": "Washington Capitals",
        "Winnipeg": "Winnipeg Jets"
    }
        
    df['Away Team'] = df['Away Team'].map(team_map)
    df['Home Team'] = df['Home Team'].map(team_map)

    # DROPPING NA FOR NON NHL SPECIAL MATCHES
    df = df.dropna(axis='index',how='any')

    # SORTING THE COLUMNS FOR ALPHABETIC ORDER
    df['team1'], df['team2'] = zip(*df.apply(lambda row: sorted([row['Away Team'], row['Home Team']]), axis=1))

    # SELECTING SORTED COLUMNS
    df = df[['data','team1','team2']]

    # CONCATENATING TO FORM MATCH STRING
    df.loc[:, 'game'] = df['team1'] + ' x ' + df['team2']
    
    # KEEP 2 COLUMNS ONLY
    df = df[['data','game']]
    
    df.to_csv(csv_output, index=False)

    # # ALLOW ALL COLUMNS TO BE PRINTED
    # pd.set_option('display.max_rows', None)

    # print(df)

if __name__ == "__main__":
    transform('data/json', 'data/all_games.csv')