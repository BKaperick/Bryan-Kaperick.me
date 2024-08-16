import json
import datetime
import os
import sys
sys.path.append(os.path.abspath("../../"))
from helper import *

count = 1
with open("photos.json", "r+") as fw:
    photos = json.load(fw)
    for file in os.listdir("./new/"):
        print(file)
        name_words = [clean_key(w) for w in file.replace(".txt", "").replace(".jpg", "").split("_")]
        longest_word = max(name_words, key=len)
        name_guess = " ".join(name_words)
        name_guess = name_guess[0].capitalize() + name_guess[1:]
        year = datetime.datetime.now().year
        if count == 1:
            last_photo = max([(k,v) for k,v in photos.items() if v['year'] == year], key=lambda x : x[1]['order_in_year'])
            if last_photo:
                order_in_year = last_photo[1]['order_in_year'] + 1
                count = order_in_year 

        d = {
            "rawpath": "./photos/raw/" + file,
            "month": str(datetime.datetime.now().strftime("%B"))[:3],
            "year": datetime.datetime.now().year,
            "order_in_year": count,
            "en": "",
            "fr": "",
            "people": ["bryan"],
            }
        nickname = longest_word + '_' + str(count) if longest_word in photos.keys() else longest_word
    
        photos[nickname] = d
        count += 1
        
        os.rename("./new/" + file, "./raw/" + file)

    fw.seek(0)
    json.dump(photos, fw, indent=4)
    fw.truncate()
