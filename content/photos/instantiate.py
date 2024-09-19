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
    if len(sys.argv[1].split("\r\n")) >= 2:
        en_trad,fr_trad = sys.argv[1].split("\r\n")[:2]
    else:
        en_trad,fr_trad = sys.argv[1].split(r"\r\n")[:2]

def instantiate_album(photos, basepath):
    count = 1
    for file in os.listdir(basepath):
        if file == '__empty__.txt':
            continue

        path = os.path.join(basepath, file)
        if os.path.isdir(path):
            # skip directories
            continue

        print("file: " + file)
        name_words = [clean_key(w) for w in file.replace(".txt", "").replace(".jpeg", "").replace(".jpg", "").split("_")]
        longest_word = max(name_words, key=len)
        name_guess = " ".join(name_words)
        name_guess = name_guess[0].capitalize() + name_guess[1:]
        year = datetime.datetime.now().year
        if count == 1 and photos:
            last_photo = max([(k,v) for k,v in photos.items() if v['year'] == year], key=lambda x : x[1]['order_in_year'])
            if last_photo:
                order_in_year = last_photo[1]['order_in_year'] + 1
                count = order_in_year 

        d = {
            "name": file,
            "month": str(datetime.datetime.now().strftime("%B"))[:3],
            "year": datetime.datetime.now().year,
            "order_in_year": count,
            "en": en_trad,
            "fr": fr_trad,
            "people": ["bryan"],
            }
        nickname = longest_word + '_' + str(count) if longest_word in photos.keys() else longest_word
    
        photos[nickname] = d
        count += 1
        print("{0} photo keys present".format(len(photos.keys())))

        os.rename(basepath + "/" + file, basepath.replace("/new/","/raw/") + file)
    return photos

with open("photos.json", "r+") as fw:
    photos = json.load(fw)
    print("{0} photo keys present at start".format(len(photos.keys())))
    basepath = "./new/"
    
    albums = []
    for file in os.listdir(basepath):
        path = os.path.join(basepath, file)
        if os.path.isdir(path):
            albums.append((file,path))
    
    # First handle any individual photos added
    photos = instantiate_album(photos, basepath)

    for name,path in albums:
        print(name, path)
        print(photos)
        photos[name] = instantiate_album({}, path)
        
    
    fw.seek(0)
    json.dump(photos, fw, indent=4)
    fw.truncate()
