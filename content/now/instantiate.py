import json
import datetime
import os
import sys
sys.path.append(os.path.abspath("../../"))
from helper import *

en_trad = ""
fr_trad = ""

# When called from a github action, we pass the PR body comment to this script,
# the first line being the english translation, and the second line being the french one.
if len(sys.argv) > 1 and sys.argv[1]:
    if len(sys.argv[1].split("\r\n")) >= 3:
        location,en_trad,fr_trad = sys.argv[1].split("\r\n")[:3]
    else:
        location,en_trad,fr_trad = sys.argv[1].split(r"\r\n")[:3]

count = 1
with open("now.json", "r+") as fw:
    nows = json.load(fw)
    print("{0} now keys present at start".format(len(nows.keys())))
    file = [f for f in os.listdir("./new/") if not '.txt' in f][0]
    print("file: " + file)
    name_words = [clean_key(w) for w in file.replace(".txt", "").replace(".jpg", "").split("_")]
    longest_word = max(name_words, key=len)
    name_guess = " ".join(name_words)
    name_guess = name_guess[0].capitalize() + name_guess[1:]

    d = {
        "location": location,
        "date": str(datetime.datetime.now().strftime("%Y-%m-%d")),
        "en": en_trad,
        "fr": fr_trad,
        "photo": file
    }
    nickname = longest_word + '_' + str(count) if longest_word in nows.keys() else longest_word

    nows[nickname] = d
    count += 1
    print("{0} now keys present".format(len(nows.keys())))
    
    os.rename("./new/" + file, "./raw/" + file)

    fw.seek(0)
    json.dump(nows, fw, indent=4)
    fw.truncate()
