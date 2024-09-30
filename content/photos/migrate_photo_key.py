import json
import os
import sys
from math import sqrt,floor
sys.path.append(os.path.abspath("../../"))
from helper import *

before, after = sys.ARGV[1:]
with open("photos.json", "rw") as fw:
    photos = json.load(fw)
    album_photos = []
    if before not in photos.keys():
        throw new Exception("Key not found: '{0}'".format(before));
    photos[after] = photos[before]
    del photos[before]
    
    fw.seek(0)
    json.dump(photos, fw, indent=4)
    fw.truncate()
    os.rename("./", "path/to/new/destination/for/file.foo")
