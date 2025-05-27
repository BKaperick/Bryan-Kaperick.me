import json
import os
import sys
import math
from math import sqrt,floor
sys.path.append(os.path.abspath("../../"))
from helper import *

name_to_cleaned = {
    "cecile": "Cécile",
    "floriane": "Flo",
    "julie": "Julie S.",
    "remy_blabla": "Remy"
}

class Score:
    count = 0
    inv_weight = 0
    def __init__(self):
        pass
        

def clean_name(name):
    if name in name_to_cleaned:
        return name_to_cleaned[name]
    else:
        return name[0].upper() + name[1:]

def get_leaderboard(year = None, metric = "inv_weight"):
    leaderboard = dict()
    leaderboard_invweighted = dict()
    with open("photos.json", "r") as fw:
        photos = json.load(fw)
        album_photos = []
        count = 0
        for key,photo in photos.items():
            if "is_album" in photo and photo["is_album"] == True:
                continue
            if year != None and photo["year"] != year:
                continue
            count += 1
            for person in photo["people"]:
                if not person in leaderboard:
                    leaderboard[person] = Score()
                leaderboard[person].count += 1
                leaderboard[person].inv_weight += 1 / math.log(1 + len(photo["people"]))

    del leaderboard["bryan"]
    leaders = [(clean_name(k),v) for k,v in leaderboard.items()]
    ranked = sorted(leaders, key= lambda x : getattr(x[1], "inv_weight"))
    return ranked, count

def get_leaderboard_winner(year = None, metric = "inv_weight"):
    ranked_year, count_year = get_leaderboard(year, metric = metric)
    if len(ranked_year) >= 1:
        winner, winner_score = ranked_year[-1]
        winner_metric = getattr(winner_score, metric)
        if len(ranked_year) > 1 and winner_metric == getattr(ranked_year[-2][1], metric):
            winner = ", ".join(sorted([w[0] for w in ranked_year if getattr(w[1], metric) == winner_metric]))
    return winner, winner_metric

if __name__ == '__main__':
    metric = "inv_weight"
    ranked,count = get_leaderboard(metric = metric)
    for year in range(2017, 2026):
        winner, winner_metric = get_leaderboard_winner(year, metric)
        print("winner in {0}: {1} - {2} photos".format(year, winner, winner_metric))
    print("\n".join(["{0} - {1}".format(x[0], getattr(x[1], metric)) for x in ranked]))

