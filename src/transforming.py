import json
import os 
import pandas as pd
from datetime import timedelta

# Carregar o arquivo JSON
path_to_json = 'data/json/'

# Lista para armazenar os dados dos jogos
games_list = []

for file_name in [file for file in os.listdir(path_to_json) if file.endswith('.json')]:
    with open(path_to_json + file_name) as file:

        data = json.load(file)

    # Extrair a lista de jogos
    game_weeks = data.get('gameWeek', [])

    # Iterar sobre cada semana de jogos
    for game_week in game_weeks:
        games = game_week.get('games', [])   
        # Iterar sobre cada jogo
        for game in games:
            game_data = {
                'data': game.get('startTimeUTC'),
                'Away Team': game.get('awayTeam', {}).get('placeName', {}).get('default', ''),
                'Home Team': game.get('homeTeam', {}).get('placeName', {}).get('default', '')
            }
            games_list.append(game_data)


# Criar o DataFrame
df = pd.DataFrame(games_list)

# Reorganizar as colunas
df = df[['data', 'Away Team', 'Home Team']]


df['data'] = pd.to_datetime(df['data'], format='%Y-%m-%dT%H:%M:%SZ')
df['data'] = df['data'] - timedelta(hours=3)

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

# DROPPING NA FOR WEIRD GAME
df = df.dropna(axis='index',how='any')

# SORTING THE COLUMNS FOR ALPHABETIC ORDER
df['team1'], df['team2'] = zip(*df.apply(lambda row: sorted([row['Away Team'], row['Home Team']]), axis=1))

# SELECTING SORTED COLUMNS
df = df[['data','team1','team2']]

# CONCATENATING TO FORM CONFRONTATIONS
df.loc[:, 'game'] = df['team1'] + ' x ' + df['team2']
df = df[['data','game']]

df.to_csv("data/all_games.csv", index=False)

# # Exibir o DataFrame
# pd.set_option('display.max_rows', None)

# print(df)

