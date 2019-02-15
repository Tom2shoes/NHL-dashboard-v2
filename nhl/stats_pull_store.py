# Dependencies
import requests
import pandas as pd

from pandas.io.json import json_normalize
from pymongo import MongoClient

# # Remote MongoDB 
# # OLD CHANGE THIS @@@@@@@@@@@@
# client = MongoClient('mongodb://nhldashboard:password1@ds215370.mlab.com:15370/heroku_5gkg84qp')
# db = client['heroku_5gkg84qp']
# collection = db['RANK']
# collection.drop()

# Local MongoDB
client = MongoClient('localhost', 27017)
db = client['nhl-database']
collection = db['RANK']
collection.drop()

# Endpoint with team ID's
team_endpoint = 'https://statsapi.web.nhl.com/api/v1/teams'
teams_response = requests.get(team_endpoint).json()

# Collects the team ID's into a list
team_ids = []

for x in range(len(teams_response['teams'])):
    team_ids.append(teams_response['teams'][x]['id'])

# Uses the collected ids to loop through endpoints of team statistics & copy to MongoDB
for team in team_ids:
    query_url = f"https://statsapi.web.nhl.com/api/v1/teams/{team}/stats"
    team_stats = requests.get(query_url).json()
    collection.insert(team_stats)
