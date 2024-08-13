import json
import os
import datetime


count = 1
with open("poems.json", "r+") as fw:
    poems = json.load(fw)

    for file in os.listdir("./new/"):
        print(file)
        name_words = file.replace(".txt", "").split("_")
        longest_word = max(name_words, key=len)
        name_guess = " ".join(name_words)
        name_guess = name_guess[0].capitalize() + name_guess[1:]
        d = {
            "title": name_guess,
            "author": "Bryan Kaperick",
            "month": str(datetime.datetime.now().strftime("%B"))[:3],
            "year": str(datetime.datetime.now().year),
            "rawpath": "./raw/" + file,
            "order_in_month": 1
            }
        nickname = longest_word + '_' + str(count) if longest_word in poems.keys() else longest_word
    
        poems[nickname] = d
        count += 1
        
        os.rename("./new/" + file, "./raw/" + file)

    fw.seek(0)
    json.dump(poems, fw, indent=4)
    fw.truncate()
