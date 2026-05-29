import json
import os
import datetime


count = 1
with open("posts.json", "r+") as fw:
    posts = json.load(fw)

    for file in os.listdir("./new/"):
        if file == "__empty__.txt":
            continue
        print(file)
        name_words = file.replace(".txt", "").split("_")
        longest_word = max(name_words, key=len)
        name_guess = " ".join(name_words)
        name_guess = name_guess[0].capitalize() + name_guess[1:]
        d = {
            "title": open(file, "r").readline(),
            "author": "Bryan Kaperick",
            "time": str(datetime.datetime.now()),
            "day": str(datetime.datetime.now().day),
            "month": str(datetime.datetime.now().strftime("%B"))[:3],
            "year": str(datetime.datetime.now().year),
            "tags": [],
            "rawpath": "./raw/" + file,
            "order_in_month": 1,
        }
        nickname = (
            longest_word + "_" + str(count)
            if longest_word in posts.keys()
            else longest_word
        )

        posts[nickname] = d
        count += 1

        os.rename("./new/" + file, "./raw/" + file)

    fw.seek(0)
    json.dump(posts, fw, indent=4)
    fw.truncate()
