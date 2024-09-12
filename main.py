from src.fights import process_fights_data
from src.webscrapping import NhlScrapper
from src.transforming import transform
from src.final_model import model
import datetime

# GETTING THE STATS
all_time_fights =  "data/nhl-regular-all-fights.csv"
all_time_fights_stats_output = "data/fight_stats.csv"
all_time_top50 = "data/top50_fights.csv"

process_fights_data(all_time_fights, all_time_fights_stats_output, all_time_top50)

# -----------------------------------------------------------------------------------------
# SCRAP THE SEASON SCHEDULE

# DEFINE START AND END DATE FOR SEASON
startdate = datetime.date(2024, 9, 21) # INCLUDING PRE-SEASON
enddate = datetime.date(2025, 4, 12)

# INSTANCE SCRAPPER
scrapper = NhlScrapper()

# GENERATE WEEKS LIST
gameweeks = scrapper.generate_gameweeks(startdate, enddate)

# LOOP EACH GAME WEEK, CALLS API AND SAVES DATA
for week in gameweeks:
    scrapper.gameweek = week
    games = scrapper.call_api()
    if games:
        scrapper.extract_data(games, week)

# -----------------------------------------------------------------------------------------
# TRANSFORM

json_dir = 'data/json'
all_games =  'data/all_games.csv'
transform(json_dir, all_games)

# -----------------------------------------------------------------------------------------
# FINAL MODELLING

final_model =  'data/games_of_interest.csv'
model(all_games, all_time_top50, final_model )