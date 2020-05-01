import requests
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup


def game_date():
    """Gets current in-game date"""
    headers = {"User-Agent":
         "Mozilla/5.0 (X11; CrOS x86+64 8172.45.0) AppleWebKit/537.36"}
    page_response = requests.get("http://atractor.net/worldnews/index.php",
                                 headers=headers)
    soup = BeautifulSoup(page_response.content, features="html.parser")
    game_date_string = soup.find('div', { "class" : "WorldInfo" }).contents[-5].text
    game_date = datetime.strptime(game_date_string.split(", ")[0], "%d %b")
    return game_date  # datetime object from the string grabbed off the webpage


def time_until_harvest():
    """Calculates real-time minutes until in-game harvest date"""
    harvest_day = datetime.strptime("1901 30 Aug", "%Y %d %b")  # harcoded because it does not change
    game_time_multiplier = 9.8630137 # in-game day takes just under 10 minutes of real time to pass
    days_remaining = harvest_day - game_date()  # in-game days remaining until harvest day
    minutes_remaining = days_remaining.days * game_time_multiplier  # converts game-days into real-minutes
    time_until_harvest = timedelta(minutes = int(minutes_remaining))
    return time_until_harvest  # timedelta of real time from now until in-game harvest
