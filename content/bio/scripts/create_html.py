import json
import os
import sys
from math import sqrt,floor
sys.path.append(os.path.abspath("../../"))
from helper import *
from datetime import datetime
current_year = datetime.now().year

def create_book_block(key, book):
    authors = ", ".join([a["name"] for a in book["authors"]])
    return """<li><em><?=$p->{0}->title;?></em> &ndash; {1}</li>
    """.format(key, authors)

with open("books.json", "r") as fr:
    books = json.load(fr)
    blocks = []
    for key,book in books.items():
        block = create_book_block(key, book)
        blocks.append(block)
    books_html = "<ul>\n" + "\n".join(blocks) + "\n<\\ul>"
    with open("books.html", "w") as p:
        p.write(books_html)
