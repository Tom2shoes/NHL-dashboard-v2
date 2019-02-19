from flask import Flask, render_template, jsonify
from flask_pymongo import PyMongo
import pandas as pd
from pandas.io.json import json_normalize
import requests

# # Remote
# # OLD CHANGE THIS @@@@@@@@@@@@
# app = Flask(__name__)
# app.config["MONGO_URI"] = "mongodb://nhldashboard:password1@ds215370.mlab.com:15370/heroku_5gkg84qp"
# mongo = PyMongo(app)

# Local
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/nhl-database"
mongo = PyMongo(app)

rank_data = mongo.db.RANK.find({})
mongo_df = pd.DataFrame(list(rank_data))


@app.route("/")
def landing_page():
    return render_template("index.html")

@app.route("/playerstats/<searchid>")
def playerstats(searchid):

    # for team in team_list:
    #     for player in team['roster']:
    #         if playername == player['person']['fullName']:
    #             try:
    #                 search_team.append(team)
    #                 search_team = search_team[0]['team']
                    
    #                 search_id = player['person']['id']
    #             except:
    #                 pass


    player_data = []

    stats_url = f"https://statsapi.web.nhl.com/api/v1/people/{searchid}/stats?stats=yearByYear"
    player_all_seasons = requests.get(stats_url).json()
    all_stats = player_all_seasons['stats'][0]['splits']

    nhl_stats = []

    for season in range(len(all_stats)):
        if all_stats[season]['league']['name'] == 'National Hockey League':
            nhl_stats.append(all_stats[season])
        else:
            next


    return jsonify(nhl_stats[-1])

if __name__ == "__main__":
    app.run(debug=True)
