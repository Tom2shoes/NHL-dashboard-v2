from flask import Flask, render_template, jsonify
from flask_pymongo import PyMongo
import pandas as pd
from pandas.io.json import json_normalize

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

pre_df_list = []
for i in range(31):
    pre_df_list.append((mongo_df.stats[i][1]['splits'][0]))

stats_df = json_normalize(pre_df_list)
stats_df.iloc[:, :28] = stats_df.iloc[:, :28].replace('\w\w$', '', regex=True)
rank_df = stats_df


@app.route("/")
def landing_page():
    return render_template("index.html",
                           teamsList=rank_df['team.name'].values.tolist())


# Route for radar chart data
@app.route("/chartData")
def test():
    rank_df['stat.pts'] = pd.to_numeric(rank_df['stat.pts'])
    rank_df['stat.faceOffWinPercentage'] = pd.to_numeric(rank_df['stat.faceOffWinPercentage'])
    rank_df['stat.goalsPerGame'] = pd.to_numeric(rank_df['stat.goalsPerGame'])
    rank_df['stat.shootingPctRank'] = pd.to_numeric(rank_df['stat.shootingPctRank'])
    rank_df['stat.wins'] = pd.to_numeric(rank_df['stat.wins'])

    df_to_json = {
            "teamName": rank_df['team.name'].values.tolist(),
            "pts": rank_df['stat.pts'].values.tolist(),
            "faceOffWinPercentage": rank_df['stat.faceOffWinPercentage'].values.tolist(),
            "goalsPerGame": rank_df['stat.goalsPerGame'].values.tolist(),
            "shootingPctRank": rank_df['stat.shootingPctRank'].values.tolist(),
            "wins": rank_df['stat.wins'].values.tolist()
            }

    return jsonify(df_to_json)


# Route to display radar chart
@app.route("/teamstats")
def team_stats():
    return render_template("radar.html", 
                           teamsList=rank_df['team.name'].values.tolist())


@app.route("/latestgame/<team>")
def away_page(team):
    game_data = []

    data = mongo.db.BOXSCORES.find({
        "$or": [
            {'away_team': team},
            {'home_team': team}
        ],
        'home_shots': {"$gt": 0},
        'away_shots': {"$gt": 0}}).sort([('game_id', -1)]).limit(1)

    for stat in data:
        game_data = {
            "game id": stat["game_id"],
            "Home Goals": stat["home_goals"],
            "Home Shots": stat["home_shots"],
            "Home Penalty Minutes": stat["home_pim"],
            "Home Takeaways": stat["home_takeaway"],
            "Home Team": stat["home_team"],
            "Home Giveaways": stat["home_giveaway"],
            "Away Team": stat["away_team"],
            "Away Goals": stat["away_goals"],
            "Away Shots": stat["away_shots"],
            "Away Penalty Minutes": stat["away_pim"],
            "Away Takeaways": stat["away_takeaway"],
            "Away Giveaways": stat["away_giveaway"]
        }

    if game_data["Home Shots"] == 0:
        return ("Game not yet played")
    else:
        return render_template("gametable.html",
                               team=team,
                               game_data=game_data,
                               teamsList=rank_df['team.name'].values.tolist())


if __name__ == "__main__":
    app.run(debug=True)
