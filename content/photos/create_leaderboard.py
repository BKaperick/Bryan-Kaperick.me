import json
import os
import sys
from math import sqrt,floor
sys.path.append(os.path.abspath("../../"))
from helper import *

def get_leaderboard(min_cutoff = 2):
    leaderboard = dict()
    with open("photos.json", "r") as fw:
        photos = json.load(fw)
        album_photos = []
        for key,photo in photos.items():
            if "is_album" in photo and photo["is_album"] == True:
                continue
            for person in photo["people"]:
                if not person in leaderboard:
                    leaderboard[person] = 0
                leaderboard[person] += 1
    leaders = [(k,v) for k,v in leaderboard.items() if v >= min_cutoff]
    ranked = sorted(leaders, key= lambda x : x[1])
    return ranked

if __name__ == '__main__':
    ranked = get_leaderboard()
    print(ranked)
    print("\n".join(["{0} - {1}".format(x[0], x[1]) for x in ranked]))
