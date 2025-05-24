import json
import os
import sys
from math import sqrt,floor
sys.path.append(os.path.abspath("../../"))
from helper import *

name_to_cleaned = {
    "cecile": "Cécile",
    "floriane": "Flo",
    "julie": "Julie S.",
    "remy_blabla": "Remy"
}

def clean_name(name):
    if name in name_to_cleaned:
        return name_to_cleaned[name]
    else:
        return name[0].upper() + name[1:]

def get_leaderboard(year = None, min_cutoff = 1):
    print(year)
    leaderboard = dict()
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
            print(key, photo["people"])
            for person in photo["people"]:
                if not person in leaderboard:
                    leaderboard[person] = 0
                leaderboard[person] += 1
    del leaderboard["bryan"]
    leaders = [(clean_name(k),v) for k,v in leaderboard.items() if v >= min_cutoff]
    ranked = sorted(leaders, key= lambda x : x[1])
    return ranked, count

if __name__ == '__main__':
    ranked,count = get_leaderboard()
    for year in range(2017, 2026):
        ranked_year, count_year = get_leaderboard(year)
        if len(ranked_year) > 1:
            winner, winner_cnt = ranked_year[-1]
            if winner_cnt > ranked_year[-2][1]:
                winner = ", ".join([w[0] for w in ranked_year if w[1] == winner_cnt])
            print("winner in {0}: {1} - {2} photos ({3})".format(year, winner, winner_cnt, f"{winner_cnt/count_year:.0%}"))
    print(ranked)
    print("\n".join(["{0} - {1}".format(x[0], x[1]) for x in ranked]))

