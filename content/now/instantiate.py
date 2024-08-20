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
    print(sys.argv)
    print(sys.argv[1])
    date,location,en_trad,fr_trad = sys.argv[1].split("\r\n")

count = 1
with open("now.json", "r+") as fw:
    nows = json.load(fw)
    print("{0} now keys present at start".format(len(nows.keys())))
    for file in os.listdir("./new/"):
        if file == '__empty__.txt':
            continue
        print("file: " + file)
        name_words = [clean_key(w) for w in file.replace(".txt", "").replace(".jpg", "").split("_")]
        longest_word = max(name_words, key=len)
        name_guess = " ".join(name_words)
        name_guess = name_guess[0].capitalize() + name_guess[1:]
        year = datetime.datetime.now().year
        if count == 1:
            last_now = max([(k,v) for k,v in nows.items() if v['year'] == year], key=lambda x : x[1]['order_in_year'])
            if last_now:
                order_in_year = last_now[1]['order_in_year'] + 1
                count = order_in_year 

        d = {
            "location": 
            "name": file,
            "month": str(datetime.datetime.now().strftime("%Y-%M-%D")),
            "en": en_trad,
            "fr": fr_trad
        }
        nickname = longest_word + '_' + str(count) if longest_word in nows.keys() else longest_word
    
        nows[nickname] = d
        count += 1
        print("{0} now keys present".format(len(nows.keys())))
        
        os.rename("./new/" + file, "./raw/" + file)

    fw.seek(0)
    json.dump(nows, fw, indent=4)
    fw.truncate()
