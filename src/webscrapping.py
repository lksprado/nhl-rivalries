import datetime
import json
import os

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


class NhlScrapper:
    def __init__(self):
        self.origin = "https://api-web.nhle.com/v1/schedule"
        self.http = self._configure_session()
        self.gameweek = ""
        self.data_dir = "data/json/"

    # SETTING A A REQUESTS.SESSION OBJECT WITH CUSTOM CONFIGURATION TO HANDLE HTTP REQUESTS
    def _configure_session(self):
        retry_strategy = Retry(
            total=3,  # HOW MANY RETRIES
            status_forcelist=[
                403,
                429,
                500,
                502,
                503,
                504,
            ],  # FOR THESE STATUS CODE FAILURE
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)  # CONTROLS THE REQUEST CALLS
        session = (
            requests.Session()
        )  # TO PERSIST SESSION VARIABLES FOR THE FOLLOWING REQUESTS
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session

    # LISTING ALL GAME WEEKS TO QUERY
    def generate_gameweeks(self, startdate, enddate):
        gameweeks_ls = []
        current_date = startdate
        while current_date <= enddate:
            gameweeks_ls.append(current_date.strftime("%Y-%m-%d"))
            current_date += datetime.timedelta(days=7)
        return gameweeks_ls

    def call_api(self):
        url = f"{self.origin}/{self.gameweek}"
        print(f"Request URL: {url}")  # FOR DEBUGGING
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0"
        }
        try:
            response = self.http.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(
                    f"Failed to retrieve data for {self.gameweek}. Status code: {response.status_code}"
                )
                return None

        except Exception as e:
            print(f"Error during API call: {e}")
            return None

    def extract_data(self, games, gameweek):
        # SAVES JSON TO DIR 'data/'
        file_path = os.path.join(self.data_dir, f"{gameweek}.json")
        with open(file_path, "w") as json_file:
            json.dump(games, json_file, indent=4)
        print(f"Data for {gameweek} saved to {file_path}")


if __name__ == "__main__":
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
