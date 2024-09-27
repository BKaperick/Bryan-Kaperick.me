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

def set_initial_count(photos):
    '''
    Find the existing photos from this year and set count to be strictly larger
    '''
    count = 1
    year = datetime.datetime.now().year
    if len(photos) > 0:
        last_photo = max([(k,v) for k,v in photos.items() if v['year'] == year], key=lambda x : x[1]['order_in_year'])
        if last_photo:
            order_in_year = last_photo[1]['order_in_year'] + 1
            count = order_in_year 
    return count

def get_nickname(photo_keys, file):
    name_words = [clean_key(w) for w in file.lower().replace(".txt", "").replace(".jpeg", "").replace(".jpg", "").split("_")]
    longest_word = max(name_words, key=len)
    nickname = longest_word + '_' + str(count) if longest_word in photo_keys else longest_word
    return nickname


def instantiate_image(photo_keys, file, count):
    print("file: " + file)

    d = {
        "name": file,
        "month": str(datetime.datetime.now().strftime("%B"))[:3],
        "year": datetime.datetime.now().year,
        "order_in_year": count,
        "en": en_trad,
        "fr": fr_trad,
        "people": ["bryan"],
        "is_album": False
        }
    nickname = get_nickname(photo_keys, file)
    return nickname, d 

def move_photo_file(basepath, file):
    directory = "./raw/"
    #directory = basepath.replace("/new/","/raw/")
    #directory = basepath.replace("/new/","/raw/") + "/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.rename(basepath + "/" + file, directory + file)

def instantiate_album(photos, basepath, name):
    count = set_initial_count(photos)
    album_d = {
        "name": name,
        "month": str(datetime.datetime.now().strftime("%B"))[:3],
        "year": datetime.datetime.now().year,
        "order_in_year": count,
        "en": en_trad,
        "fr": fr_trad,
        "is_album": True,
        "photos": []
        }
    for file in os.listdir(basepath):
        
        # skip directories and __empty__ placeholder file
        path = os.path.join(basepath, file)
        if (file == '__empty__.txt') or os.path.isdir(path):
            continue

        fixed_file = file.replace(".JPG", ".jpg").replace(".jpeg", ".jpg").replace(".JPEG", ".jpg")
        
        nickname, d = instantiate_image(photos.keys(), fixed_file, count)
        photos[nickname] = d
        album_d["photos"].append(nickname)
        move_photo_file(basepath, fixed_file)
        count += 1
    return album_d

    #print("{0} photo keys present".format(len(photos.keys())))
    #return photos
    
def instantiate_dir(photos, basepath, name = ""):
    count = set_initial_count(photos)
    for file in os.listdir(basepath):
        
        # skip directories and __empty__ placeholder file
        path = os.path.join(basepath, file)
        if (file == '__empty__.txt') or os.path.isdir(path):
            continue
        
        nickname, d = instantiate_image(photos.keys(), file, count)

        photos[nickname] = d
        move_photo_file(basepath, file)
        count += 1

    print("{0} photo keys present".format(len(photos.keys())))
    return photos

with open("photos.json", "r+") as fw:
    photos = json.load(fw)
    print("{0} photo keys present at start".format(len(photos.keys())))
    basepath = "./new/"
    
    # Any directories are treated as a photo album
    albums = []
    for file in os.listdir(basepath):
        path = os.path.join(basepath, file)
        if os.path.isdir(path):
            albums.append((file,path))
    
    # First handle any individual photos added
    photos = instantiate_dir(photos, basepath)

    for name,path in albums:
        photos[name] = instantiate_album(photos, path, name)
        
    
    fw.seek(0)
    json.dump(photos, fw, indent=4)
    fw.truncate()
