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
def date_getter(b):
    month = int(b["personal"]["finish_month"]) if "finish_month" in b["personal"] else 0
    year = 100 * int(b["personal"]["finish_year"])
    return year + month

with open("books.json", "r") as fr:
    books = json.load(fr)
    blocks = []
    limit = None
    if len(sys.argv) > 1:
        limit = int(sys.argv[1])
    books = books.items()
    ordered_books = sorted(books, key=lambda b : -date_getter(b[1]))
    for i,(key,book) in enumerate(ordered_books):
        block = create_book_block(key, book)
        blocks.append(block)
    books_html = "<ul>\n" + "\n".join(blocks) + "\n</ul>"
    with open("books.html", "w") as p:
        p.write(books_html)
