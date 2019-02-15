import requests
from pymongo import MongoClient
import pprint
pp = pprint.PrettyPrinter(indent=1)

url = "https://statsapi.web.nhl.com/api/v1/game/"


url = "https://statsapi.web.nhl.com/api/v1/schedule?startDate=2018-10-03&endDate=2018-12-10"
game_ids = requests.get(url).json()


# Retrieve all game_ids from the start of the 2018 season to partway through the season

all_game_ids = []

for y in range(len(game_ids["dates"])):
    for x in range(len(game_ids["dates"][y]["games"])):
        game_id = game_ids["dates"][y]["games"][x]["gamePk"]
        #print(game_id)
        all_game_ids.append(game_id)

client = MongoClient('localhost', 27017)
db = client['nhl-database']

# Retrieve data from NHL API and put into MongoDB

url = "https://statsapi.web.nhl.com/api/v1/game/"


collection = db['BOXSCORES']
collection.drop()
collection = db['BOXSCORES']

for game in all_game_ids:
    query_url = f"{url}{game}/feed/live"
    game_info = requests.get(query_url).json()
    
    try:
        game_data = {}
        game_data['game_id'] = game
        
        game_data['home_team'] = game_info["liveData"]["boxscore"]["teams"]["home"]["team"]["name"]
        game_data['home_goals'] = game_info["liveData"]["boxscore"]["teams"]["home"]["teamStats"]["teamSkaterStats"]["goals"]
        game_data['home_shots'] = game_info["liveData"]["boxscore"]["teams"]["home"]["teamStats"]["teamSkaterStats"]["shots"]
        game_data['home_pim'] = game_info["liveData"]["boxscore"]["teams"]["home"]["teamStats"]["teamSkaterStats"]["pim"]
        game_data['home_takeaway'] = game_info["liveData"]["boxscore"]["teams"]["home"]["teamStats"]["teamSkaterStats"]["takeaways"]
        game_data['home_giveaway'] = game_info["liveData"]["boxscore"]["teams"]["home"]["teamStats"]["teamSkaterStats"]["giveaways"]
        
        game_data['away_team'] = game_info["liveData"]["boxscore"]["teams"]["away"]["team"]["name"]
        game_data['away_goals'] = game_info["liveData"]["boxscore"]["teams"]["away"]["teamStats"]["teamSkaterStats"]["goals"]
        game_data['away_shots'] = game_info["liveData"]["boxscore"]["teams"]["away"]["teamStats"]["teamSkaterStats"]["shots"]
        game_data['away_pim'] = game_info["liveData"]["boxscore"]["teams"]["away"]["teamStats"]["teamSkaterStats"]["pim"]
        game_data['away_takeaway'] = game_info["liveData"]["boxscore"]["teams"]["away"]["teamStats"]["teamSkaterStats"]["takeaways"]
        game_data['away_giveaway'] = game_info["liveData"]["boxscore"]["teams"]["away"]["teamStats"]["teamSkaterStats"]["giveaways"]
              
        collection.insert(game_data)
        
        print(f"Collecting data for {game}.")
        print("------------------------------")
        
    except:
        pass
        print(f"Error for {game}.")
        print("Moving onto next game...")
        print("------------------------------")

