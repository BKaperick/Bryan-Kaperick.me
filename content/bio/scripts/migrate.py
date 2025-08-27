import json
import os
import sys
sys.path.append(os.path.abspath("../../"))
from helper import *

with open("books.json", "r+") as fw:
    books = json.load(fw)
    for key,book in books.items():
        # Add new field 'status' with default value
        if not "status" in book["personal"]:
            book["personal"]["status"] = "completed"
    
    fw.seek(0)
    json.dump(books, fw, indent=4)
    fw.truncate()
